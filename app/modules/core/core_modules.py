"""Core module sigleton access module."""


def get_controls(parent=None):
    """Return controls singleton core module."""
    # from controls.view import Controls
    # return Controls(parent)
    pass


def get_live_viewer(parent=None):
    """Return live viewer singleton core module."""
    from live_viewer.view import LiveViewer
    return LiveViewer(parent)


def get_previewer(parent=None):
    """Return previewer singleton core module."""
    from previewer.view import Previewer
    return Previewer(parent)


def get_status_bar(parent=None):
    """Return statusbar singleton core module."""
    from statusbar.view import StatusBar
    return StatusBar(parent)


def get_toolbox(parent=None):
    """Return toolbox singleton core module."""
    from toolbox.view import ToolBox
    return ToolBox(parent)
