'''
Created on Sep 10, 2013

@author: fli
'''
from urlparse import urlparse

_TOP_DOMAINS = ['com', 'edu', 'gov', 'int', 'mil', 'net', 'org', 'biz', 'info', 'pro', 'name', 'museum',\
        'coop', 'aero', 'idv', 'xxx']

def get_fuzzy_domains(url):
    ''' get hosts '''
    u = urlparse(url)
    keys = []
    keys.append(u.netloc)
    paths = u.path.split('/')
    keys.extend(paths)
    keys = [x for x in keys if x != '']
    hosts = []
    i = 1
    for _ in keys:
        hosts.append('/'.join(keys[0:i]))
        i += 1
    domain_frags = u.netloc.lower().split('.')
    while len(domain_frags) >= 2:
        if len(domain_frags) == 2 and domain_frags[0] in _TOP_DOMAINS:
            break
        domain = '.'.join(domain_frags)
        if domain == u.netloc:
            domain_frags.pop(0)
            continue
        hosts.insert(0, domain)
        domain_frags.pop(0)
    return reversed(hosts)
