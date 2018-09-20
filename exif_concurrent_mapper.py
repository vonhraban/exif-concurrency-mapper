from multiprocessing import Process
from gps_coordinates import extractor, writer
from http_server import server
import os
import webbrowser
from threading import Thread
import atexit
import sys

def get_coordinates_for_folder(folder):
    # build up a list of absolute file paths in the directory
    files = list(map(lambda x: os.path.abspath(os.path.join(folder, x)), os.listdir(folder)))
    coordinates_list = list(map(extractor.get_coordinates, files))
    # filter out empty coordinates that happen if file has no gps data attached
    return list(filter(lambda x: x != {}, coordinates_list))


def link_files(folder):
    '''
    Links files so that they can be served by the server
    :return:
    '''
    source_absolute = os.path.abspath(folder)
    target_absolute = os.path.abspath('./static/source')
    if source_absolute is not target_absolute:
        os.symlink(source_absolute, target_absolute)


def unlink_files():
    '''
    Removes the symlink
    :return:
    '''
    os.unlink(os.path.abspath('./static/source'))

def cleanup():
    print("Exiting")
    unlink_files()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: %s <folder>" % sys.argv[0])
        sys.exit(1)

    folder = sys.argv[1]

    if not os.path.isdir(folder):
        print("Error: Directory %s not found" % folder)
        sys.exit(1)

    atexit.register(cleanup)
    coordinates = get_coordinates_for_folder(folder)
    writer = writer.Writer()
    writer.as_geojson(coordinates)
    link_files(folder)
    thread = Thread(target=server.create)
    thread.start()

    webbrowser.open(server.get_url(), new=2)

