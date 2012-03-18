import os, logging
from tempfile import mkdtemp
from subprocess import Popen, PIPE
from threading import Thread
from shutil import rmtree
from collections import namedtuple

from sauce.model import Assignment, Submission, Language, Compiler, Interpreter, Test, TestRun, DBSession as Session

#from sauce.lib.runner.compiler import compile
#from sauce.lib.runner.interpreter import interpret

log = logging.getLogger(__name__)

process = namedtuple('process', ['returncode', 'stdout', 'stderr'])

# Timeout value for join between sending SIGTERM and SIGKILL to process
THREADKILLTIMEOUT = 0.5

class CompileFirstException(Exception): pass

class TimeoutProcess():
    '''Runs an external command until timeout is reached
    
    Assumes that Popen uses PIPE for stdin, stdout and stderr
    Data for stdin may be supplied on instantiation, stdout and
    stderr will be returned from the call.'''
    
    def __init__(self):
        self.argv = None
        self.timeout = None
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.p = None
        self.t = None
    
    def __call__(self, argv, timeout, stdin=None, **kwargs):
        '''Run external command argv until timeout is reached
        
        If stdin is not none the data will be supplied to the
        processes stdin
        Remaining kwargs will be passed to Popen'''
        
        self.argv = argv
        self.timeout = timeout
        self.stdin = stdin
        
        def target():
            self.p = Popen(self.argv, stdin=PIPE, stdout=PIPE, stderr=PIPE, **kwargs)
            (self.stdout, self.stderr) = self.p.communicate(self.stdin)
        
        self.t = Thread(target=target)
        self.t.start()
        self.t.join(self.timeout)
        
        if self.t.isAlive():
            log.debug("Terminating process %d in thread %s" % (self.p.pid, self.t.name))
            self.p.terminate()
            self.t.join(THREADKILLTIMEOUT)
            if self.t.isAlive():
                log.debug("Killing process %d in thread %s" % (self.p.pid, self.t.name))
                self.p.kill()
        
        return process(self.p.returncode, self.stdout, self.stderr)

def compile(compiler, dir, srcfile, objfile):
    '''Compiles a source file
    
    @param compiler: Compiler object
    @param dir: Working directory
    @param srcfile: Filename of source file
    @param objfile: Filename of object file
    
    @return: (returncode, stdoutdata, stderrdata)
    '''
    
    tp = TimeoutProcess()
    
    # Get compiler information
    log.debug('Compiler: %s' % compiler)
    
    # Assemble compiler command line
    #log.debug('%s' % compiler.argv)
    a = compiler.argv.replace('{srcfile}', os.path.join(dir, srcfile))
    a = a.replace('{objfile}', os.path.join(dir, objfile))
    #log.debug('%s' % a)
    
    args = [compiler.path]
    args.extend(a.split())
    
    log.debug('Command line: %s' % args)
    
    # Run compiler
    (returncode, stdoutdata, stderrdata) = tp(args, timeout=compiler.timeout, 
                                              # This overrides all other environment variables
                                              cwd=dir, env={'LC_ALL': 'C'}, 
                                              shell=False)
    
    log.debug('Process returned: %d' % returncode)
    log.debug('Process stdout: %s' % stdoutdata.strip())
    log.debug('Process stderr: %s' % stderrdata.strip())
    
    return process(returncode, stdoutdata, stderrdata)

def execute(interpreter, dir, binfile, timeout, stdin=None, argv=''):
    '''Execute or interpret a binfile
    
    @param interpreter: Interpreter object or none
    @param dir: Working directory
    @param binfile: Filename of executable or script file
    @param timeout: Timeout value for test run
    @param stdin: Standard input data
    @param argv: Additional argv to command line
    
    @return: (returncode, stdoutdata, stderrdata)
    '''
    
    tp = TimeoutProcess()
    
    if interpreter:
        # Get interpreter information
        log.debug('Interpreter: %s' % interpreter)
        args = [interpreter.path]
        a = interpreter.argv.replace('{srcfile}', os.path.join(dir, binfile))
        args.extend(a.split())
    else:
        args = [os.path.join(dir, binfile)]
    
    if argv:
        args.extend(argv.split())
    
    log.debug('Command line: %s' % args)
    
    # Run
    (returncode, stdoutdata, stderrdata) = tp(args, timeout=timeout, 
                                              stdin=stdin, cwd=dir,
                                              # This overrides all other environment variables 
                                              env={'LC_ALL': 'C'}, shell=False)
    
    log.debug('Process returned: %d' % returncode)
    log.debug('Process stdout: %s' % stdoutdata.strip())
    log.debug('Process stderr: %s' % stderrdata.strip())
    
    return process(returncode, stdoutdata, stderrdata)

def compareTestOutput(a, b):
    '''Compare test output a to test output b
    
    At the moment we ignore all whitespace by comparing
    the resulting arrays from .split()
    '''
    return a.split() == b.split()

class Runner():
    '''Context Manager-aware Runner class
    
    Use as:
        with Runner(submission) as runner:
            runner.compile()
            ...
            for test in runner.test():
                ...
    
    Temporary directories shall be removed on exit or
    object destruction
    
    Reminder:
    The execution order of magic methods for 
    
        with Test() as t:
            print "..."
    
    is (regardless of any exception):
    
        __init__
        __enter__
        ...
        __exit__
        __del__
    '''
    
    def __init__(self, submission):
        '''Initialize Runner object for given submission
        
        Creates temporary directory and saves source file
        '''
        
        self.submission = submission
        self.assignment = submission.assignment
        self.language = submission.language
        
        # Create temporary directory
        self.tempdir = mkdtemp()
        log.debug('tempdir: %s' % self.tempdir)
        
        # Create temporary source file
        self.tempfile = 'a%d_s%d' % (self.assignment.id, self.submission.id)
        if self.language.extension:
            self.srcfile = self.tempfile + '.' + self.language.extension
        else:
            self.srcfile = self.tempfile
        log.debug('srcfile: %s' % self.srcfile)
        
        # Write source code to source file
        with open(os.path.join(self.tempdir, self.srcfile), 'w') as srcfd:
            srcfd.write(submission.source)
    
    def __enter__(self):
        '''Context Manager entry function'''
        
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        '''Context Manager exit function'''
        
        if self.tempdir:
            try:
                rmtree(self.tempdir)
            except:
                pass
            else:
                self.tempdir = None
    
    def __del__(self):
        '''Destructor function
        
        If not already deleted by __exit__ (e.g. if Runner()
        was not used as Context Manager, removes temporary directory
        '''
        
        if self.tempdir:
            try:
                rmtree(self.tempdir)
            except:
                pass
            else:
                self.tempdir = None
    
    def compile(self):
        '''Compile submission source files, if needed
        
        If submission.language doesn't specify a compiler
        to use, None is returned
        '''
        
        if self.language.compiler:
            self.compilation = compile(self.language.compiler, self.tempdir, self.srcfile, self.tempfile)
            self.binfile = self.tempfile
            return self.compilation
        else:
            self.compilation = True
            self.binfile = self.srcfile
            return None
    
    def test(self):
        '''Run all associated test cases
        
        Keeps going, even if one test fails.
        '''
        
        if self.compilation:
            for test in self.assignment.tests:
                process = execute(self.language.interpreter, self.tempdir, self.binfile, self.assignment.timeout, test.input, test.argv)
                if process.returncode == 0 and compareTestOutput(test.output, process.stdout):
                    yield True
                else: 
                    yield False
        else:
            raise CompileFirstException('Y U NO COMPILE FIRST')
