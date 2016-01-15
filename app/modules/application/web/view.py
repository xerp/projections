from PyQt4.QtCore import Qt

import app.resources.modules.web as ui_resource
import app.modules.utils as utils


def configure_options(**kwargs):
    options = WebPageOptions(kwargs['controls'].module_options_panel)
    options.set_dependents(kwargs)
    options.configure()

    return options


class WebPageOptions(utils.ApplicationModule, utils.Projectable):
    __controls = {
        'clear_text': {'cmdClearText': 'clicked()'},
        'show_web': {'txtWebPage': 'returnPressed()'},
        'writing_web_page': {'txtWebPage': 'textChanged (const QString&)'}
    }

    def __init__(self, parent):
        utils.ApplicationModule.__init__(self, parent, None, ui_resource.Ui_Form(), self.__controls)
        utils.Projectable.__init__(self, 'url')

    def config_components(self):

        self._widget.youtubeOptions.setVisible(False)
        self.callback('clear_text', self.__clear_text)
        self.callback('show_web', self.__show_web)
        self.callback('writing_web_page', self.__writing_page)


    def configure(self):

        self._controls.history_control = self._widget.txtWebPage.setText
        self._controls.add_module_options(self)
        self._controls.set_enable_slides(False)
        self._controls.enable_live_font = False
        self._previewer.setVisible(False)

        self._widget.txtWebPage.setFocus()
        self._statusbar.set_status('Web page module loaded successfully')

    def __writing_page(self, text):
        self._widget.youtubeOptions.setVisible('www.youtube' in text)

    def __clear_text(self):
        self._widget.txtWebPage.clear()

    def __show_web(self):
        text = self._widget.txtWebPage.text()

        if text and self._toolbox.direct_live:
            self._toolbox.go_to_live()

    def process_projection(self, previewText, **kwargs):
        url = str(self._widget.txtWebPage.text())

        if url:
            self._controls.append_to_history(url)
            self._widget.txtWebPage.clear()

            if 'http://' not in url and 'https://' not in url:
                url = 'http://{0}'.format(url)

            if '//www.youtube' in url:
                url = url.replace('watch?v=', 'v/')

                autoplay = '1' if self._widget.chkAutoPlay.checkState() == Qt.Checked else '0'
                controls = '1' if self._widget.chkPlayerControls.checkState() == Qt.Checked else '0'

                url = '{0}?rel=0&amp;autoplay={1}&amp;controls={2}&amp;showinfo=0'.format(
                    url, autoplay, controls)

            self._set_projection_item(url)
