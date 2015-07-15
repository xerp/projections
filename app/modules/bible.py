# -*- coding: utf-8 -*-

import subprocess
import os
import re
import json
import sys
from ConfigParser import ConfigParser
from app.lib.helpers import to_unicode, to_str

import app.resources.modules.bible as ui_resource
import app.modules.utils as utils

if sys.platform == 'linux2':
    import Sword as sw

conf = ConfigParser()
conf.read('config.ini')

BIBLE_CONFIG = dict(conf.items('BIBLE'))
DELIMITER = '\n' if not conf.getboolean('BIBLE', 'use_bible_internet_service') else '\n\n'


def _call_bible_service(typ, bible_version, unicode_criteria):
    str_criteria = to_str(unicode_criteria)

    process = subprocess.Popen(
        ['java', '-jar', '{0}/bible-service.jar'.format(os.path.dirname(os.path.abspath(__file__))),
         '-{0}'.format(typ), bible_version, str_criteria], stdout=subprocess.PIPE)

    try:
        unicode_json = to_unicode(process.communicate()[0], 'latin1')
        return json.loads(unicode_json)
    except ValueError, e:
        raise BibleError(e)


def _internet_bible_search(unicode_criteria):
    try:
        unicode_dic = _call_bible_service('ref', BIBLE_CONFIG['bible_version_service'], unicode_criteria)

        unicode_bible_name = u'Reina Gómez Valera'
        unicode_module_text = unicode_dic['text']
        unicode_key_name = unicode_dic['reference']

        unicode_text = u'{0}: {1}'.format(unicode_key_name, unicode_module_text)

        return unicode_text, unicode_bible_name, unicode_key_name, unicode_module_text
    except IndexError:
        raise SearchNotFound('Search "{0}" not found'.format(unicode_criteria))
    except Exception, e:
        raise BibleError(e)


def _sword_bible_search(unicode_key_search):
    bible = BIBLE_CONFIG['default_bible']
    locale = BIBLE_CONFIG['default_locale']

    str_key_search = to_str(unicode_key_search)

    try:
        library = sw.SWMgr()
        bible_module = library.getModule(bible)
        key_module = sw.SWKey(str_key_search)
        key_module.setLocale(locale)
        bible_module.setKey(key_module)

        unicode_bible_name = to_unicode(bible_module.getDescription())
        unicode_module_text = to_unicode(bible_module.getRawEntry())
        unicode_key_name = to_unicode(bible_module.getKeyText())

    except Exception, e:
        raise BibleError(e)

    if not unicode_module_text:
        raise SearchNotFound(unicode_key_search)

    unicode_text = u'{0}: {1}'.format(unicode_key_name, unicode_module_text)

    return unicode_text, unicode_bible_name, unicode_key_name, unicode_module_text


def _bible_search(unicode_key_search, internet_service=False):
    if unicode_key_search:
        return _sword_bible_search(unicode_key_search) if not internet_service else _internet_bible_search(
            unicode_key_search)
    else:
        raise BibleError('Search criteria cannot be empty')


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

        super(SearchNotFound, self).__init__('verse {1} not found in bible'.format(key))


class BibleOptions(utils.ApplicationModule, utils.Projectable, utils.Searchable):
    __controls = {
        'previous_chapter': {'cmdPrevChapter': 'clicked()'},
        'next_chapter': {'cmdNextChapter': 'clicked()'},
        'previous_verse': {'cmdPrevVerse': 'clicked()'},
        'next_verse': {'cmdNextVerse': 'clicked()'},
        'bible_internet_service': {'chkInternetService': 'stateChanged (int)'}
    }

    def __init__(self, parent):
        utils.ApplicationModule.__init__(self, parent, None, ui_resource.Ui_bibleOptions(), self.__controls)
        utils.Projectable.__init__(self, 'text')

    def config_components(self):

        self.callback('previous_chapter', self.__previous_chapter)
        self.callback('next_chapter', self.__next_chapter)
        self.callback('previous_verse', self.__previous_verse)
        self.callback('next_verse', self.__next_verse)
        self.callback('bible_internet_service', self.__bible_internet_service)

    def configure(self):

        self._controls.search_in_history(True)
        self._controls.add_module_options(self)
        self._controls.configure_search_box(self)
        self._controls.set_enable_slides(False)

        self._widget.chkInternetService.setVisible(False)
        # Temporally Commented self._widget.chkInternetService.setChecked(conf.getboolean('BIBLE','use_bible_internet_service'))

        self._statusbar.set_status('Bible module loaded successfully')

    def __bible_internet_service(self, check):
        DELIMITER = '\n\n' if check else '\n'

    def __next_search(self):

        text = self.__current_search.split(' ')[0:-1]
        text = ' '.join(text)
        next_search = '{0} {1}:{2}'.format(text, self.__current_chapter, self.__current_verse)

        return next_search

    def __previous_chapter(self):
        if self.__current_chapter > 1:
            self.__current_chapter -= 1
            self.search(self.__next_search())

    def __next_chapter(self):

        self.__current_chapter += 1
        self.search(self.__next_search())

    def __previous_verse(self):
        if self.__current_verse > 1:
            self.__current_verse -= 1
            self.search(self.__next_search())

    def __next_verse(self):

        self.__current_verse += 1
        self.search(self.__next_search())

    def __configure_navigations(self, unicode_text):

        # If text search contains , or - navigation is disable
        disable_navigation = re.match('.*[,-]+.*', unicode_text)
        active = False if disable_navigation else True

        self._widget.cmdPrevChapter.setEnabled(active)
        self._widget.cmdNextChapter.setEnabled(active)
        self._widget.cmdPrevVerse.setEnabled(active)
        self._widget.cmdNextVerse.setEnabled(active)

        if active:
            try:
                nums = unicode_text.split(' ')[-1]
                values = nums.split(':') if ':' in nums else [1, 1]
                chapter = values[0]
                verse = values[1] if values[1] else 1

                self.__current_search = unicode_text
                self.__current_chapter = int(chapter)
                self.__current_verse = int(verse)
            except Exception:
                pass

    def search(self, text=None):

        self._controls.set_search_box_text(text)
        unicode_search_text = to_unicode(self._controls.search_box_text())

        try:

            self.entire_text, self.bible_name, self.verse_name, self.verse_text = _bible_search(unicode_search_text,
                                                                                                self._widget.chkInternetService.isChecked())
            self.__configure_navigations(unicode_search_text)
            if not text:
                self._controls.add_to_history(unicode_search_text)

            self._previewer.set_text(self.entire_text)

            if self._toolbox.direct_live:
                self._toolbox.process_projection()

            self._controls.clear_search_box()
        except BibleError, e:
            self._statusbar.set_status(str(e), True, 2)

    def process_projection(self, preview_text, **kwargs):
        template, variables = self.template('bible')

        passages = [Passage(self.verse_text, self.verse_name), ]
        image = '{0}/{1}/{2}'.format(
            self.config.get('GENERAL', 'images_dirs'),
            self.config.get('LIVE', 'backgrounds_dir'),
            self.config.get('BIBLE', 'background_image')
        )

        slide_info = self.bible_name  # Temporally commented ;self.config.get('BIBLE','bible_version_service' if self._widget.chkInternetService.isChecked() else 'default_bible')

        variables['passages'] = passages
        variables['image'] = image
        variables['slide_info'] = slide_info

        self._set_projection_item(template.render(variables))


class Passage:
    def __init__(self, unicode_text, unicode_reference=None):
        if unicode_reference:
            self.reference = unicode_reference
            self.text = unicode_text
        else:
            text = unicode_text.split(':')
            self.reference = u'{book_chapter}:{verse}'.format(book_chapter=text[0], verse=text[1])
            self.text = u''.join(text[2::]).strip()
