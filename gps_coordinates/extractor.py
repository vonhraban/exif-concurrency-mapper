# Thank you https://gist.github.com/snakeye/fdc372dbf11370fe29eb
from exifread import process_file
import os


def get_coordinates_for_folder(folder):
    # build up a list of absolute file paths in the directory
    files = list(map(lambda x: os.path.abspath(os.path.join(folder, x)), os.listdir(folder)))
    coordinates_list = list(map(get_coordinates, files))
    # filter out empty coordinates that happen if file has no gps data attached
    return list(filter(lambda x: x != {}, coordinates_list))


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def get_coordinates(filename):
    """
    Returns the latitude and longitude, if available, from the extracted exif data for the given file name
    """
    handler = open(filename, 'rb')
    tags = process_file(handler)
    latitude = tags.get('GPS GPSLatitude')
    latitude_ref = tags.get('GPS GPSLatitudeRef')
    longitude = tags.get('GPS GPSLongitude')
    longitude_ref = tags.get('GPS GPSLongitudeRef')
    if latitude:
        lat_value = _convert_to_degress(latitude)
        if latitude_ref.values != 'N':
            lat_value = -lat_value
    else:
        return {}
    if longitude:
        lon_value = _convert_to_degress(longitude)
        if longitude_ref.values != 'E':
            lon_value = -lon_value
    else:
        return {}
    return {'latitude': lat_value, 'longitude': lon_value}
