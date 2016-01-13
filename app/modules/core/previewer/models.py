"""Previewer model module."""

from app.libraries.modules import AbstractModel
from app.libraries.encoding import to_unicode
# from app.libraries.ui import get_projection_font


class PreviewerModel(AbstractModel):
    """PreviewerModel class."""

    def __init__(self, view):
        """PreviewerModel Constructor."""
        AbstractModel.__init__(self, view)

    def configure_module(self):
        """Configure module."""
        # self.setFont(get_projection_font(dict(self.config.items(
        #   'FONT_PREVIEW')), self.config.getint('LIVE', 'DEFAULT_FONT_SIZE')))
        pass

    def set_text(self, text):
        """
            Set text.

        Parameters:
            * text: text to set
        """
        self._view.setText(text if isinstance(
            text, unicode) else to_unicode(text))

    def reset(self):
        """Reset previewer text."""
        self._view.set_text('')
        self._view.setVisible(True)
        self._view.setEnabled(True)
