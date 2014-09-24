from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.resources.modules.bible as ui_resource
import app.modules.utils as utils

def configure_options(controls):

    options = BibleOptions(controls.module_options_panel)
    
    controls.add_module_options(options)
    controls.configure_search_box()

    return options

class BibleError(Exception):
    pass

class SearchNotFound(BibleError):
    def __init__(self, type_search, key):
        self.type_search = type_search
        self.key = key

        super(SearchNotFound, self).__init__('{0} {1} not found in bible'.format(type_search, key))

class BibleOptions(utils.AbstractModule):

    def __init__(self,parent):
        utils.AbstractModule.__init__(self,parent,None,ui_resource.Ui_bibleOptions())

    def instance_variable(self):
        utils.AbstractModule.instance_variable(self)


    def config_components(self):
        pass     

# import subprocess
# from ConfigParser import ConfigParser

# conf = ConfigParser()
# conf.read('config.ini')

# BIBLE_CONFIG = dict(conf.items('BIBLE_EXTERNAL_APP'))
# DELIMITER = '\n'

# def _call_command(command, args):
#     proc = subprocess.Popen('{0} {1}'.format(command, args),
#                             shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

#     return proc.stdout.read(), proc.stderr.read()


# def _bible_search(type_search, key_search):
#     bible = BIBLE_CONFIG['default_bible']
#     locale = BIBLE_CONFIG['default_locale']

#     args = BIBLE_CONFIG['bible_command_args'].format(
#         bible_version=bible,
#         locale=locale,
#         type_search=type_search,
#         key=key_search)

#     try:
#         result, errors = _call_command(BIBLE_CONFIG['bible_command'], args)

#         if errors:
#             errors = '{0}...'.format(' '.join(errors.split('\n'))[:60])
#             raise BibleError(errors)

#     except Exception, e:
#         raise BibleError(e)

#     if result == '({bible})\n'.format(bible=bible) or 'none ({bible})\n'.format(bible=bible) in result:
#         raise SearchNotFound(type_search, key_search)
#     else:
#         return result


# def search_verse(verse):
#     result = _bible_search('verse', verse)

#     result = result.replace(BIBLE_CONFIG['default_bible'], 'END')
#     return result.decode('latin')


# def search_phrase(phrase):
#     result = _bible_search('phrase', phrase)
#     return result.decode('latin')

