import subprocess
import re
from ConfigParser import ConfigParser

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import app.resources.modules.bible as ui_resource
import app.modules.utils as utils

conf = ConfigParser()
conf.read('config.ini')

BIBLE_CONFIG = dict(conf.items('BIBLE'))
DELIMITER = '\n'

def _call_command(command, args):
    proc = subprocess.Popen('{0} {1}'.format(command, args),
                            shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    return proc.stdout.read(), proc.stderr.read()


def _bible_search(type_search, key_search):
    bible = BIBLE_CONFIG['default_bible']
    locale = BIBLE_CONFIG['default_locale']

    args = BIBLE_CONFIG['bible_command_args'].format(
        bible_version=bible,
        locale=locale,
        type_search=type_search,
        key=key_search)

    try:
        result, errors = _call_command(BIBLE_CONFIG['bible_command'], args)

        if errors:
            errors = '{0}...'.format(' '.join(errors.split('\n'))[:60])
            raise BibleError(errors)

    except Exception, e:
        raise BibleError(e)

    if result == '({bible})\n'.format(bible=bible) or 'none ({bible})\n'.format(bible=bible) in result:
        raise SearchNotFound(type_search, key_search)
    else:
        return result

def configure_options(*args):

    options = BibleOptions(args[0].module_options_panel)
    options.set_dependents({
        'controls' :args[0],
        'statusbar' :args[1],
        'previewer' : args[2],
        'liveViewer' : args[3],
        'toolbox' : args[4]
        })

    options.configure()

    return options

class BibleError(Exception):
    pass

class SearchNotFound(BibleError):
    def __init__(self, type_search, key):
        self.type_search = type_search
        self.key = key

        super(SearchNotFound, self).__init__('{0} {1} not found in bible'.format(type_search, key))

class BibleOptions(utils.AbstractModule):

    __controls = {
        'search_forward': {'cbSearchForward':'stateChanged(int)'},
        'previous_chapter':{'cmdPrevChapter':'clicked()'},
        'next_chapter':{'cmdNextChapter':'clicked()'},
        'previous_verse':{'cmdPrevVerse':'clicked()'},
        'next_verse':{'cmdNextVerse':'clicked()'}
    }

    def __init__(self,parent):
        utils.AbstractModule.__init__(self,parent,None,ui_resource.Ui_bibleOptions(),self.__controls)

    def instance_variable(self):
        utils.AbstractModule.instance_variable(self)

    def config_components(self):
        search_forward = self.config.getboolean('BIBLE', 'search_forward')
        self._widget.cbSearchForward.setChecked(search_forward)
        self._widget.sbForwardLimit.setEnabled(search_forward)

        self._widget.sbForwardLimit.setValue(self.config.getint('BIBLE', 'forward_limit'))

        self.callback('search_forward',self.__search_forward)

        self.callback('previous_chapter',self.__previous_chapter)
        self.callback('next_chapter',self.__next_chapter)
        self.callback('previous_verse',self.__previous_verse)
        self.callback('next_verse',self.__next_verse)

    def configure(self):

        self._controls.add_module_options(self)
        self._controls.configure_search_box(self.__bible_search)

        self._statusbar.set_status('Bible module loaded successfully')

    def __search_forward(self,value):
        self._widget.sbForwardLimit.setEnabled(value == 2)

    def __next_search(self):

        text = str(self.__current_search).split(' ')[::-2]
        text = ' '.join(text)
        next_search = '{0} {1}:{2}'.format(text,self.__current_chapter,self.__current_verse)
        print next_search
        return next_search

    def __previous_chapter(self):
        if self.__current_chapter > 1:

            self.__current_chapter -= 1
            self.__next_search()

    def __next_chapter(self):

        self.__current_chapter += 1
        self.__next_search()

    def __previous_verse(self):
        if self.__current_verse > 1:

            self.__current_verse -= 1
            self.__next_search()

    def __next_verse(self):

        self.__current_verse += 1
        self.__next_search()

    def __configure_navigations(self,text):

        #If text search contains , or - navigation is disable
        disable_navigation = re.match('.*[,-]+.*', text)
        active = False if disable_navigation else True

        self._widget.cmdPrevChapter.setEnabled(active)
        self._widget.cmdNextChapter.setEnabled(active)
        self._widget.cmdPrevVerse.setEnabled(active)
        self._widget.cmdNextVerse.setEnabled(active)

        if active:
            try:
                nums = text.split(' ')[-1]
                values = nums.split(':') if ':' in nums else [1,1]
                chapter = values[0]
                verse = values[1] if values[1] else 1

                self.__current_search = text
                self.__current_chapter = chapter
                self.__current_verse = verse
            except Exception:
                pass

    def __search_verse(self,verse):
        result = _bible_search('verse', verse)

        result = result.replace(BIBLE_CONFIG['default_bible'], 'END')
        return result.decode('latin')

    def __search_phrase(self,phrase):
        result = _bible_search('phrase', phrase)
        return result.decode('latin')

    def __bible_search(self,text = None):

        self._controls.set_search_box_text(text)
        search_text = self._controls.search_box_text()
        result = ''

        self.__configure_navigations(search_text)

        if self._widget.cbSearchForward.isChecked():
            search_text = '{0}-'.format(search_text)

        try:
            result = self.__search_verse(search_text)
        except BibleError, e:
            self._statusbar.set_status(str(e), True)

        self._previewer.set_text(result)

        self._controls.set_slides(result, DELIMITER,self._widget.sbForwardLimit.value())

        if self._toolbox.direct_live:
            self._liveViewer.set_text(self.slides[self._controls.slide_position],self._controls.live_font())
        
        self._controls.clear_search_box()