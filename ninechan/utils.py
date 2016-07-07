import hashlib
import random
import string

__author__ = 'takeshix'
__all__ = [
    'validate_xss_easy',
    'validate_xss_hard',
    'escape_xss_strings',
    'generate_session_token',
    'secure_filename']


def validate_xss_easy(string):
    if '<script>' in string:
        return False
    return True


def validate_xss_hard(string):
    if not validate_xss_easy(string):
        return False

    if 'alert(' in string:
        return False

    return True

def escape_xss_strings(string):
    pass


def generate_session_token():
    return random_hex_string(size=16)


def random_string(size=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in xrange(8))


def random_hex_string(size=8):
    return ''.join(random.choice(string.hexdigits) for _ in xrange(8))


def secure_filename(name):
    """Generates a secure filename for uploaded files."""
    hasher = hashlib.md5()
    hasher.update('{}{}\o/'.format(random_string(),name))
    return hasher.hexdigest()