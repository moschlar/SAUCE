import os, logging
from tempfile import mkdtemp
from subprocess import Popen, PIPE
from threading import Thread
from shutil import rmtree
from collections import namedtuple

from sauce.model import Assignment, Submission, Language, Compiler, Interpreter, Test, TestRun, DBSession as Session
import transaction

#from sauce.lib.runner.compiler import compile
#from sauce.lib.runner.interpreter import interpret

log = logging.getLogger(__name__)

process = namedtuple('process', ['returncode', 'stdout', 'stderr'])

# Timeout value for join between sending SIGTERM and SIGKILL to process
THREADKILLTIMEOUT = 0.5

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
    (returncode, stdoutdata, stderrdata) = tp(args, timeout=compiler.timeout, cwd=dir, shell=False)
    
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
    (returncode, stdoutdata, stderrdata) = tp(args, timeout=timeout, stdin=stdin, cwd=dir, shell=False)
    
    log.debug('Process returned: %d' % returncode)
    log.debug('Process stdout: %s' % stdoutdata.strip())
    log.debug('Process stderr: %s' % stderrdata.strip())
    
    return process(returncode, stdoutdata, stderrdata)

class Runner():
    '''
    
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
        return self
    
    def __del__(self):
        if self.tempdir:
            rmtree(self.tempdir)
            self.tempdir = None
    
    def __exit__(self, exception_type, exception_value, traceback):
        if self.tempdir:
            rmtree(self.tempdir)
            self.tempdir = None
    
    def compile(self):
        if self.language.compiler:
            self.compilation = compile(self.language.compiler, self.tempdir, self.srcfile, self.tempfile)
            self.binfile = self.tempfile
            return self.compilation
        else:
            self.compilation = True
            self.binfile = self.srcfile
            return None
    
    def test(self):
        if self.compilation:
            for test in self.assignment.tests:
                yield execute(self.language.interpreter, self.tempdir, self.binfile, self.assignment.timeout, test.input, test.argv)
        else:
            raise Exception('Y U NO COMPILE FIRST')

def run(submission):
    """Runs a submission
    
    All tests associated with the submitted assignment will
    be executed until one fails
    
    Returns a tuple of (exit status, stdoutdata, stderrdata)"""
    
    #tp = TimeoutProcess()
    
    # Easier names for variables
    assignment = submission.assignment
    language = submission.language
    compiler = language.compiler
    interpreter = language.interpreter
    tests = assignment.tests
    
    # Create temporary directory
    tempdir = mkdtemp()
    log.debug('tempdir: %s' % tempdir)
    
    # Create temporary source file
    tempfile = '%d_%d' % (assignment.id, submission.id)
    if language.extension:
        srcfile = tempfile + '.' + language.extension
    else:
        srcfile = tempfile
    log.debug('srcfile: %s' % srcfile)
    
    # Write source code to source file
    with open(os.path.join(tempdir, srcfile), 'w') as srcfd:
        srcfd.write(submission.source)
    
    # Compile if needed
    if compiler:
        # Use tempfile as filename for executable
        (returncode, stdoutdata, stderrdata) = compile(compiler, tempdir, srcfile, tempfile)
        if returncode != 0:
            # Compilation failed
            return False
        binfile = tempfile
    else:
        binfile = srcfile
    
    # Run, using interpreter if needed
    for test in tests:
        testrun = TestRun(test, submission)
        Session.add(testrun)
        
        p = execute(interpreter, tempdir, binfile, assignment.timeout, test.input, test.argv)
        
        # Split output for whitespace insensitive comparison
        log.debug('Output matches: %s' % (test.output.split() == p.stdout.split()))
        if (test.output.split() != p.stdout.split()):
            rmtree(tempdir)
            testrun.result=False
            Session.commit()
            return False
        testrun.result = True
        Session.commit()
    rmtree(tempdir)
    return True
