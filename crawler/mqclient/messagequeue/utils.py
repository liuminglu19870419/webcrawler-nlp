'''
Created on Dec 12, 2012

@author: fli
'''
import datetime
import calendar

def datetime2timestamp(dt):
    '''
    Converts a datetime object to UNIX timestamp in milliseconds.
    '''
    if hasattr(dt, 'utctimetuple'):
        t = calendar.timegm(dt.utctimetuple())
        timestamp = int(t) + float(dt.microsecond) / 1000000
        return timestamp * 1000
    return dt

def datetime2microtimestamp(dt):
    '''
    Converts a datetime object to UNIX timestamp in milliseconds.
    '''
    if hasattr(dt, 'utctimetuple'):
        t = calendar.timegm(dt.utctimetuple())
        timestamp = int(t)*1000000 + dt.microsecond
        return timestamp
    return dt

def timestamp2datetime(timestamp):
    '''
    Converts UNIX timestamp in milliseconds to a datetime object.
    '''
    if isinstance(timestamp, (int, long, float)):
        return datetime.datetime.utcfromtimestamp(timestamp / 1000)
    return timestamp

def load_object(path):
    """Load an object given its absolute object path, and return it.

    object can be a class, function, variable o instance.
    path ie: 'scrapy.contrib.downloadermiddelware.redirect.RedirectMiddleware'
    """

    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot+1:]
    try:
        mod = __import__(module, {}, {}, [''])
    except ImportError, err:
        raise ImportError("Error loading object '%s': %s" % (path, err))

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj
