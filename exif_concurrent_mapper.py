from multiprocessing import Process
from gps_coordinates import extractor
from http_server import server
import os
import webbrowser
from threading import Thread


def get_coordinates_for_folder(folder):
    # build up a list of absolute file paths in the directory
    files = list(map(lambda x: os.path.abspath(os.path.join(folder, x)), os.listdir(folder)))
    coordinates_list = list(map(extractor.get_coordinates, files))
    # filter out empty coordinates that happen if file has no gps data attached
    return list(filter(lambda x: x != {}, coordinates_list))


if __name__ == '__main__':
    coordinates = get_coordinates_for_folder('./files')
    thread = Thread(target=server.create)
    thread.start()

    webbrowser.open(server.get_url(), new=2)

    # If they are not already there, copy over images to server dir
    # Or symlink?
    # Write points to a JSON file
    # Spin up a new webserver
    # Display index
    # On interruption, kill webserver