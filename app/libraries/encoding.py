"""Module with encoding functions."""


def get_default_encoding(pretty=False):
    """
    Return default enconding.

    Paremeter:
        * pretty: if return a pretty format of enconding
    """
    return 'UTF-8' if pretty else 'utf8'


def to_unicode(text, encoding=get_default_encoding(), errors='strict'):
    """Convert text to unicode."""
    return unicode(text, encoding, errors)


def to_str(text, encoding=get_default_encoding(), errors='strict'):
    """Convert text to str."""
    return str(text.encode(encoding, errors))
