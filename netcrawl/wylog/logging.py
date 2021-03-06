'''
Created on Mar 4, 2017

@author: Wyko
'''

from datetime import datetime
import os, traceback, time, sys

from netcrawl import config


# Variables for logging
CRITICAL = 1
C = 1
ALERT = 2
A = 2
HIGH = 3
H = 3
NORMAL = 4
N = 4

# Debuging levels
INFORMATIONAL = 5
I = 5
DEBUG = 6
D = 6

        
def log(msg, **kwargs):
    """
    Writes a message to the log.
    
    Args:
        msg (str): The message to write.
        
    Keyword Args:
        ip (str): The IP address of whatever device we are connected to
        proc (str): The process which caused the log entry, in the form
            of *'module.method_name'*
        log_path (str): The filepath of the directory where to save the 
            log file. Uses config.cc.log_path by default
        print_out (bool): If True, copies the message to console
        v (int): Verbosity level. Logs with verbosity above the global 
            verbosity level will not be printed out.  
            v= 1: Critical alerts
            v= 2: Non-critical alerts
            v= 3: High level info
            v= 4: Common info
            v= 5-6: Debug level info
            
        error (Exception): An exception object to be included in the
            log output
        
    Returns:
        bool: True if write was successful.
    """ 
    
    v = kwargs.get('v', 4)
    proc= kwargs.get('proc', '')
    ip= kwargs.get('ip', '') 
    error=  kwargs.get('error')
    print_out= kwargs.get('print_out', True)
    log_path = kwargs.get('log_path', config.cc.log_path)
    new_log = kwargs.get('new_log', False)
    
    # Skip debug messages (unless turned on)
    if (v >= 5) and (config.cc.debug is False): return False 
    
    msg= str(msg)
    
    # Set the prefix for the log entry
    if v >=3: info_str = '#' + str(v)
    if v ==2: info_str = '? '
    if v ==1: info_str = '! '

    msg = info_str + ' ' + msg
    
    try:
        output = '{_proc:20}, {_msg}, {_time}, {_ip:15}, {_error}'.format(
                    _time= datetime.now().strftime(config.cc.pretty_time),
                    _proc= str(proc),
                    _msg = msg.replace(',', ';'),
                    _ip = str(ip),
                    _error = str(error)
                    )
    except: pass
    
    # Print the message to console            
    try: 
        if v <=  config.cc.verbosity and print_out: print('{:<35.35}: {}'.format(proc, msg))
    except: pass
    
    if not os.path.exists(config.cc.run_path):
        os.makedirs(config.cc.run_path)
    
    # Open the error log
    if new_log: f = open(log_path, 'w')
    else: f = open(log_path, 'a')
    
    if f and not f.closed:
        f.write(output + '\n')
        f.close()
        return True
    
    else: return False
        

class log_snip():
    def __init__(self, proc, v=5):
        self.proc = proc
        self.v= v
        
    def __enter__(self):
        log('Entering snippet [{}]'.format(self.proc),
            proc= self.proc, v= self.v)
        self.start = time.time()
        
    def __exit__(self,ty,val,tb):
        end = time.time()
        
        if ty is None:
            log('Finished snippet [{}] after [{:.3f}] without error'.format(
                self.proc, end-self.start), proc= self.proc, v= self.v)
            
        else:
            log('Finished snippet [{}] after [{:.3f}] seconds with [{}] error. Traceback: [{}]'.format(
                self.proc, end-self.start, ty.__name__, traceback.format_tb(tb)),
                proc= self.proc, v= self.v)

def logf(f, **kwargs):
    parent= kwargs.get('parent', '__________')
    
    # Take a decorated method and log it.
    def wrapped_f(*args, **kwargs):
        log('Starting method [{}]'.format(f.__name__),
            proc= '{0}.{1}'.format(parent, f.__name__),
            v= DEBUG)
        start = time.time()
        
        # Run the decorated function
        try: result= f(*args, **kwargs)
        
        # On exception, log it and re-raise
        except Exception as e:
            tb = sys.exc_info()[2]
            log('Finished method [{}] after [{:.3f}] seconds with [{}] Error: [{}] Traceback: [{}]'.format(
                f.__name__, time.time()- start, type(e).__name__, str(e), traceback.format_tb(tb)),
                proc= '{0}.{1}'.format(parent, f.__name__),
                v= ALERT)
            raise
        else:
            log('Finished method [{}] after [{:.3f}] seconds'.format(
                f.__name__, time.time()- start),
                proc= '{0}.{1}'.format(parent, f.__name__),
                v= DEBUG)
            return result
    return wrapped_f