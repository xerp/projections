"""Classes and helper functions of User Interface."""

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


def get_projection_font(font_properties, default_font_size):
    """Return projection font."""
    font = QtGui.QFont(font_properties.get('name', 'arial'))
    font.setPointSize(int(font_properties.get('size', default_font_size)))
    font.setBold(bool(font_properties.get('bold', False)))
    font.setWeight(int(font_properties.get('weight', 75)))

    return font


def get_screens_count():
    """Return screens count."""
    return QtGui.QApplication.instance().desktop().numScreens()


def set_alignment(text_edit, desired_alignment):
    """Set desired_alignment for text_edit component."""
    # Make sure the cursor is at the start of the text field
    text_edit.moveCursor(QtGui.QTextCursor.Start)

    last_position = -1
    curr_position = text_edit.textCursor().position()

    while last_position != curr_position:
        text_edit.setAlignment(desired_alignment)
        text_edit.moveCursor(QtGui.QTextCursor.Down)
        last_position = curr_position
        curr_position = text_edit.textCursor().position()

    # Move to the end of the text field in preparation for whatever comes next
    text_edit.moveCursor(QtGui.QTextCursor.End)


class ProjectionWizardPage(QtGui.QWizardPage):
    """ProjectionWizardPage class."""

    def __init__(self, wizard, title):
        """ProjectionWizardPage constructor."""
        QtGui.QWizardPage.__init__(self, wizard)
        self.setTitle(title)
        self.__layout = QtGui.QVBoxLayout()
        self.setLayout(self.__layout)
        self._callbacks = {}

    def add_widget(self, widget):
        """Add widget to page layout."""
        self.__layout.addWidget(widget)

    def callback(self, event, callback):
        """Refister a callback."""
        self._callbacks[event] = callback

    def validatePage(self):
        """Validate page."""
        if 'validate' in self._callbacks:
            return self._callbacks['validate']()
        else:
            return True


class AbstractProjectionLinealDataModel(QtCore.QAbstractListModel):
    """Abstract Data Model."""

    def __init__(self, data_list=[], parent=None):
        """Class constructor."""
        QtCore.QAbstractListModel.__init__(self, None)

        self.__parent = parent
        self.data_list = data_list

    def parent(self, *args, **kwargs):
        """Return parent."""
        return self.__parent

    def rowCount(self, parent=QtCore.QModelIndex):
        """Return row count."""
        return len(self.data_list)

    def selected(self):
        """Return selected row."""
        try:
            return self.data_list[self.parent().currentIndex()]
        except (AttributeError, IndexError):
            pass


class ImageViewModel(AbstractProjectionLinealDataModel):
    """Image View Model Class."""

    def data(self, index, role=Qt.DisplayRole):
        """Return data."""
        if index.isValid():
            image = self.data_list[index.row()]

            if role == Qt.DisplayRole:
                print 'gh'
            elif role == Qt.DecorationRole:
                return QtGui.QIcon(image)
