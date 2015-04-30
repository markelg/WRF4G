"""
Print information about the hosts available on WRF4G.
     
Usage: 
    wrf4g host [ list ] [ --dbg ] [ <hid> ] 
    
Arguments:
    <hid>         Host identifier.

Options:
    --dbg         Debug mode.        
 
Host field information:
    HID           Host identifier.
    ARCH          Architecture.
    JOBS(R/T)     Number of jobs: R = running, T = total.
    LRMS          Local Resource Management System.
    HOSTNAME      Host name. 
    QUEUENAME     Queue name.
    WALLT         Queue wall time.
    CPUT          Queue cpu time.
    MAXR          Max. running jobs.
    MAXQ          Max. queued jobs. 
"""
__version__  = '2.3.1'
__author__   = 'Carlos Blanco'
__revision__ = "$Id: host.py 2352 2015-02-24 10:23:57Z carlos $"

import logging
from wrf4g                import logger
from drm4g                import DRM4G_BIN
from drm4g.commands       import exec_cmd, Daemon

def run( arg ):
    if arg[ '--dbg' ] :
        logger.setLevel(logging.DEBUG)
    try :
        daemon = Daemon()
        if not daemon.is_alive() :
            raise Exception('DRM4G is stopped.')
        cmd = '%s/gwhost '  % ( DRM4G_BIN )
        if arg[ '<hid>' ] :
            cmd = cmd + arg[ '<hid>' ]
        out , err = exec_cmd( cmd )
        logger.info( out )
        if err :
            logger.info( err )
    except Exception , err :
        logger.error( str( err ) )
