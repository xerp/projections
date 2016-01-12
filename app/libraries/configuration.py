'''
[GENERAL]
title : Renuevo Projection Manager

images_dirs : /home/santiago/Documents/Iglesia/Proyeccion/Pictures
default_image : Horario.jpg
options_to_exclude:
template_path : /home/santiago/Development/python/projections/templates
default_option : bible


[FONT_PREVIEW]
name : arial
size : 20
weight : 75
bold : yes

[LIVE]
backgrounds_dir: Fondos
default_color : black
default_text_color : white
default_text_shadow_color : black
default_background_color : black
default_font_size : 80
default_screen : 1

[BIBLE]
forward_limit : 20
search_forward: no
background_image : bible.jpg
use_bible_internet_service: no
bible_version_service: spa-RVR60

default_bible : SpaRVG
default_locale : es


[SONG]
management_font_size: 10
background_image: fondo 3.jpg
'''

import os
import orm

from ConfigParser import ConfigParser
from utils import get_user_app_directory
from data import QUERIES


# def get_app_config():
#     config = ConfigParser()
#     config.read(os.environ['config_file'])
#     return config


def get_user_database_file():
    """Return database file name path."""
    return os.path.join(get_user_app_directory(), 'projections.db')


def exists_user_database_file():
    """Return if user database exists."""
    database = get_user_database_file()
    return database and os.path.isfile(database)


def create_user_database():
    """Create the user database."""
    engine = orm.connect_to_engine(get_user_database_file(), orm.SQLITE)
    session = orm.get_session(engine)

    session.execute(QUERIES['artist_create'])
    session.execute(QUERIES['song_create'])


def check_user_database():
    """Check if user database exists to create it."""
    if not exists_user_database_file():
        create_user_database()


def get_user_configuration_file():
    """Return user configuration file path."""
    return os.path.join(get_user_app_directory(), 'user_config.ini')


def get_user_configuration():
    """Return user configuration."""
    filename = get_user_configuration_file()
    if filename and os.path.isfile(filename):
        config = ConfigParser()
        config.read(filename)
        return config


def set_user_configuration(section_dic):
    """Set the user configuration."""
    file_name = get_user_configuration_file()

    with open(file_name, 'w') as cfg_file:
        config = ConfigParser()

        for section in section_dic.keys():
            config.add_section(section)

            for variable in section_dic[section].keys():
                config.set(section, variable, section_dic[section][variable])

        config.write(cfg_file)


def get_application_geometry():
    """Return application geometry dictionary."""
    # Default Geometry
    geometry = {'x': 50,
                'y': 50,
                'width': 900,
                'height': 600}

    config = get_user_configuration()
    if config:
        try:
            geometry['x'] = config.getfloat('LOCATION', 'x')
            geometry['y'] = config.getfloat('LOCATION', 'y')
            geometry['width'] = config.getfloat('SIZE', 'width')
            geometry['height'] = config.getfloat('SIZE', 'height')
        except Exception:
            pass

    return geometry


def set_application_geometry(geometry):
    """Set application geometry config."""
    configuration = {'LOCATION':
                     {'x': geometry.x(), 'y': geometry.y()},
                     'SIZE':
                     {'width': geometry.width(), 'height': geometry.height()}}

    set_user_configuration(configuration)
