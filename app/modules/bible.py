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

def configure_options(**kwargs):

    options = BibleOptions(kwargs['controls'].module_options_panel)
    options.set_dependents(kwargs)
    options.configure()

    return options

class BibleError(Exception):
    pass

class SearchNotFound(BibleError):
    def __init__(self, type_search, key):
        self.type_search = type_search
        self.key = key

        super(SearchNotFound, self).__init__('{0} {1} not found in bible'.format(type_search, key))

class BibleOptions(utils.ApplicationModule):

    __controls = {
        'previous_chapter':{'cmdPrevChapter':'clicked()'},
        'next_chapter':{'cmdNextChapter':'clicked()'},
        'previous_verse':{'cmdPrevVerse':'clicked()'},
        'next_verse':{'cmdNextVerse':'clicked()'}
    }

    def __init__(self,parent):
        utils.ApplicationModule.__init__(self,parent,None,ui_resource.Ui_bibleOptions(),self.__controls)

    def config_components(self):

        self.callback('previous_chapter',self.__previous_chapter)
        self.callback('next_chapter',self.__next_chapter)
        self.callback('previous_verse',self.__previous_verse)
        self.callback('next_verse',self.__next_verse)

    def configure(self):

        self._controls.search_in_history(True)
        self._controls.add_module_options(self)
        self._controls.set_enable_slides(False)
        self._controls.configure_search_box(self.__bible_search)

        self._toolbox.set_go_to_live_callback(self.__go_to_live)

        self._statusbar.set_status('Bible module loaded successfully')

    def __next_search(self):

        text = self.__current_search.split(' ')[0:-1]
        text = ' '.join(text)
        next_search = '{0} {1}:{2}'.format(text,self.__current_chapter,self.__current_verse)

        return next_search

    def __previous_chapter(self):
        if self.__current_chapter > 1:

            self.__current_chapter -= 1
            self.__bible_search(self.__next_search())

    def __next_chapter(self):

        self.__current_chapter += 1
        self.__bible_search(self.__next_search())

    def __previous_verse(self):
        if self.__current_verse > 1:

            self.__current_verse -= 1
            self.__bible_search(self.__next_search())

    def __next_verse(self):

        self.__current_verse += 1
        self.__bible_search(self.__next_search())

    def __configure_navigations(self,text):

        text = str(text)
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
                self.__current_chapter = int(chapter)
                self.__current_verse = int(verse)
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

        try:
            result = self.__search_verse(search_text)
            self.__configure_navigations(search_text)
            if not text:
                self._controls.add_to_history(search_text)
        except BibleError, e:
            self._statusbar.set_status(str(e), True)

        self._previewer.set_text(result)

        if self._toolbox.direct_live:
            self._toolbox.go_to_live()

        self._controls.clear_search_box()

    def __go_to_live(self,previewText):
        text = unicode(previewText,'latin')
        template,variables = self.template('bible')

        passages = map(lambda p: Passage(p),
            filter(lambda s: s and s != '(END)',
             text.split(DELIMITER)))

        image = '{0}/{1}/{2}'.format(
            self.config.get('GENERAL','images_dirs'),
            self.config.get('LIVE','backgrounds_dir'),
            self.config.get('BIBLE','background_image')
            )

        variables['passages'] = passages
        variables['image'] = image
        variables['slide_info'] = self.config.get('BIBLE','default_bible')

        result = template.render(variables)

        return {'method':'text','text':result,'font_size':self._controls.live_font(),'encode':'latin'}

class Passage:

    def __init__(self,text):
        text = text.split(':')
        self.reference = u'{book_chapter}:{verse}'.format(book_chapter=text[0],verse=text[1])
        self.text = u''.join(text[2::]).strip()
