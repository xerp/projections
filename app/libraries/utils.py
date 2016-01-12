"""Utility module."""

import os
import sys
import subprocess


class ProjectionError(Exception):
    """ProjectionError Exception class."""


def get_user_name_home():
    """Return expanded user home dir."""
    return os.path.expanduser('~')


def get_user_app_directory():
    """Return user local directory[cross-platform]."""
    user_name_home = get_user_name_home()
    directory = ''

    # Windows
    if sys.platform == 'win32':
        directory = os.path.join(user_name_home, 'AppData\\Local\\Projections')
    # Linux
    elif sys.platform == 'linux2':
        directory = os.path.join(user_name_home, '.local/share/projections')

    if directory and not is_valid_directory(directory):
        os.mkdir(directory)

    return directory


def remove_pycs(directory):
    """
    Remove pic files over directory recursively.

    parameters:
        * directory: path name of root directory
    """
    for root, dirs, files in os.walk(directory):
        for fi in files:
            if fi[-3:] == 'pyc':
                os.remove(os.path.join(root, fi))


def get_image_files(image_directory):
    """
    Return image files of directory recursively.

    parameters:
            * image_directory: path name of root directory.
    """
    directories = image_directory.split(',')
    image_files = []

    extesions = ['.jpg', '.png']
    filter_func = lambda fi: any(fi.endswith(extension)
                                 for extension in extesions)

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            map_func = lambda fi: os.path.join(root, fi)
            filtered_list = filter(filter_func, files)
            image_files.extend(map(map_func, filtered_list))

    return image_files


def open_directory(directory):
    """Open directory through OS."""
    # Windows
    if sys.platform == 'win32':
        subprocess.Popen(['explorer', directory])

    # On Mac
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', directory])

    # Linux
    else:
        subprocess.Popen(['xdg-open', directory])


def is_valid_directory(directory):
    """Return is a valid directory."""
    return os.path.isdir(directory)
