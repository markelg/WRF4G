import os
import sys
from drm4g.global_settings import PATH_HOST, COMMUNICATOR, RESOURCE_MANAGER
from drm4g.utils.openfile import cleaner
from drm4g.utils.url import urlparse

__version__ = '0.1'
__author__  = 'Carlos Blanco'
__revision__ = "$Id: configure.py 1124 2011-08-22 08:52:04Z carlos $"

__all__ = ['ConfigureException', 'hostparse','HostConfiguration']

class ConfigureException(Exception):
    pass
  
def hostparse():
        
    path = os.path.join(os.environ['GW_LOCATION'], PATH_HOST)    
    if not os.path.exists(path): 
        raise ConfigureException('Wrong PATH_HOST')
    lines = cleaner(path)
    data_hosts = { }
    for i, line in enumerate(lines.split('\n')):
        if line :
            if len (line.split()) != 2:
                raise ConfigureException('The line %d doesn\'t have two columns' % (i))
            alias, url = line.split()
            url_result = urlparse(url)
            scheme     = url_result.scheme.lower()
            name       = url_result.host
            username   = url_result.username
            params     = url_result.params
            if not name:
                raise ConfigureException('%s doesn\'t have hostname' % (alias))
            if not username and (scheme != 'local'):
                raise ConfigureException('%s doesn\'t have username' % (alias))
            if not COMMUNICATOR.has_key(scheme):
                raise ConfigureException('%s has a wrong scheme "%s"' % (alias, scheme))
            if not params.has_key('LRMS_TYPE'):
                raise ConfigureException('%s doesn\'t have a LRMS_TYPE' % (alias))
            if not RESOURCE_MANAGER.has_key(params['LRMS_TYPE']):
                raise ConfigureException('%s has a wrong LRMS_TYPE "%s"' % (alias, params['LRMS_TYPE']))
            data_hosts [alias] = HostConfiguration(scheme, name, username, params)
    return data_hosts
                
class HostConfiguration(object):
        
    def __init__(self, scheme, name, username, params):
        
        self._scheme     = scheme
        self._name       = name
        self._username   = username
        self._params     = params
     
    def get_hostname(self):
        return self._name
              
    def get_username(self):
        return self._username
    
    def get_scheme(self):
        return self._scheme

    def get_lrms_type(self):
        return self._params['LRMS_TYPE']

    def get_node_count(self):
        return self._params.setdefault('NODECOUNT')

    def get_queue_name(self):
        return self._params.setdefault('QUEUE_NAME')

    def get_run_dir(self):
        return self._params.setdefault('GW_RUNDIR',r'~')
 
    def set_run_dir(self, run_dir):
        self._params['GW_RUNDIR'] = run_dir
        
    def get_local_dir(self):
        return self._params.setdefault('GW_LOCALDIR')
        
    def get_project(self):
        return self._params.setdefault('PROJECT')

    HOST        = property(get_hostname)
    USERNAME    = property(get_username)
    SCHEME      = property(get_scheme)
    LRMS_TYPE   = property(get_lrms_type)
    NODECOUNT   = property(get_node_count)
    QUEUE_NAME  = property(get_queue_name)
    GW_RUNDIR   = property(get_run_dir, set_run_dir)
    GW_LOCALDIR = property(get_local_dir)
    PROJECT     = property(get_project)
   