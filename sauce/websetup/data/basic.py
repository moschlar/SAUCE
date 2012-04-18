# -*- coding: utf-8 -*-
'''
Created on 18.04.2012

@author: moschlar
'''

from sauce.model import DBSession as Session, Compiler, Language, Interpreter, Compiler

def language_data(command, conf, vars):
    
    # C compiler
    cc = Compiler(name=u'GCC', path=u'/usr/bin/gcc', 
                  argv=u'-Wall {srcfile} -o {binfile}', timeout=5)
    Session.add(cc)
    
    # C language
    lc = Language(name=u'C', extension_src=u'c', compiler=cc, lexer_name=u'cpp')
    Session.add(lc)
    
    # Java compiler
    cj = Compiler(name=u'JDK', path=u'/usr/bin/javac',
                  argv=u'{srcfile}', timeout=10)
    Session.add(cj)
    
    # Java interpreter
    ij = Interpreter(name=u'JDK', path=u'/usr/bin/java',
                     argv=u'-cp {path} {basename}')
    Session.add(ij)
    
    # Java language
    lj = Language(name=u'Java 7', extension_src=u'java', extension_bin=u'class', 
                  compiler=cj, interpreter=ij, lexer_name=u'java')
    Session.add(lj)
    
    # Python interpreter
    ip = Interpreter(name=u'Python 2.7', path=u'/usr/bin/python2.7', 
                     argv=u'{binfile}')
    Session.add(ip)
    
    # Python language
    lp = Language(name=u'Python', extension_src=u'py', 
                  extension_bin=u'py', interpreter=ip, lexer_name=u'python')
    Session.add(lp)
    
    Session.flush()
    
    return (cc, lc, cj, ij, lj, ip, lp)
