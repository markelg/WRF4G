"""
Submit, get status and history and cancel jobs.

Usage: 
    drm4g job submit [ --dbg ] [ --dep <job_id> ... ] <template> 
    drm4g job list [ --dbg ] [ <job_id> ] 
    drm4g job cancel [ --dbg ]  <job_id> ... 
    drm4g job get-log [ --dbg ] <job_id>
    drm4g job get-history [ --dbg ] <job_id> 
   
Arguments:
   <job_id>               Job identifier.
   <template>             Job template.

Options:
   --dep=<job_id> ...     Define the job dependency list of the job.
   --dbg                  Debug mode.
    
Commands:
   submit                 Command for submitting jobs.
   list                   Monitor jobs previously submitted.
   cancel                 Cancel jobs.
   get-log                Keep track of a job.
   get-history            Get information about the execution history of a job.

Job field information:
   JID                    Job identification.
   DM                     Dispatch Manager state, one of: 
                                pend, hold, prol, prew, wrap, epil, canl, stop, migr, done, fail.
   EM                     Execution Manager state: pend, susp, actv, fail, done.
   START                  The time the job entered the system.
   END                    The time the job reached a final state (fail or done).
   EXEC                   Total execution time, includes suspension time in the remote queue system.
   XFER                   Total file transfer time, includes stage-in and stage-out phases.
   EXIT                   Job exit code.
   TEMPLATE               Filename of the job template used for this job.
   HOST                   Hostname where the job is being executed.
   HID                    Host identification.
   PROLOG                 Total prolog (file stage-in phase) time.
   WRAPPER                Total wrapper (execution phase) time.
   EPILOG                 Total epilog (file stage-out esphase) time.
   MIGR                   Total migration time.
   REASON                 The reason why the job left this host.
   QUEUE                  Queue name. 
"""
__version__  = '2.3.1'
__author__   = 'Carlos Blanco'
__revision__ = "$Id: job.py 2352 2015-02-24 10:23:57Z carlos $"

import logging
from drm4g                import DRM4G_BIN
from drm4g.commands       import exec_cmd, Daemon, logger 

def run( arg ) :
    if arg[ '--dbg' ] :
        logger.setLevel(logging.DEBUG)
    try :
        daemon = Daemon( )
        if not daemon.is_alive() :
            raise Exception( 'DRM4G is stopped. ')
        if arg['submit']:
            dependencies = '-d "%s"' % ' '.join( arg['--dep'] ) if arg['--dep'] else ''
            cmd = '%s/gwsubmit %s -v %s' % ( DRM4G_BIN , dependencies  , arg['<template>'] )
        elif arg['list']:
            cmd = '%s/gwps -o Jsetxjh '  % ( DRM4G_BIN )
            if arg['<job_id>'] :
                cmd = cmd + arg['<job_id>'][0] 
        elif arg['get-history']:
            cmd = '%s/gwhistory %s' % ( DRM4G_BIN , arg['<job_id>'][ 0 ] )
        elif arg['get-log']:
            directory = join(
                              DRM4G_DIR ,
                              'var' ,
                              '%d00-%d99' % ( int(int(float(arg['<job_id>'][0]))/100) , int(int(float(arg['<job_id>'][0]))/100) ) ,
                              arg['<job_id>'][0] ,
                              'job.log'
                            )
            if not exists( directory ) :
                raise Exception( 'There is not a log available for this job.')
            cmd = 'cat %s' % ( directory )
        else :
            cmd = '%s/gwkill -9 %s' % ( DRM4G_BIN , ' '.join( arg['<job_id>'] ) )  
        out , err = exec_cmd( cmd )
        logger.info( out )
        if err :
            logger.info( err )
    except Exception , err :
        logger.error( str( err ) )
