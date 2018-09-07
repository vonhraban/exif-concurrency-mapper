from multiprocessing import Process
import os
from gps_coordinates import extractor


if __name__ == '__main__':
    directory = './files'
    # build up a list of absolute file paths in the directory
    files = list(map(lambda x: os.path.abspath(os.path.join(directory, x)), os.listdir(directory)))
    print(list(map(extractor.get_coordinates, files)))

