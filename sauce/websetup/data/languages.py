'''
Created on 09.06.2012

@author: moschlar
'''

data = [
    {'Compiler': [
        {'&cj': {'name': u'JDK',
            'path': u'/usr/bin/javac',
            'argv': u'{srcfile}',
            'timeout': 10}
            },
        {'&cc': {'name': u'GCC',
            'path': u'/usr/bin/gcc',
            'argv': u'-Wall {srcfile} -o {binfile}',
            'timeout': 5}
            },
        ],
    'Interpreter': [
        {'&ij': {'name': u'JDK',
            'path': u'/usr/bin/java',
            'argv': u'-cp {path} {basename}'}
            },
        {'&ip': {'name': u'Python 2.7',
            'path': u'/usr/bin/python2.7',
            'argv': u'{binfile}'}
            },
        ],
    'flush': True,
    },
    {'Language': [
        {'&lj': {'name': u'Java',
            'lexer_name': u'java',
            'extension_src': u'java',
            'extension_bin': u'class',
            'compiler': '*cj',
            'interpreter': '*ij'}
            },
        {'&lc': {'name': u'C',
            'lexer_name': u'cpp',
            'extension_src': u'c',
            'compiler': '*cc'}
            },
        {'&lp': {'name': u'Python 2.7',
            'lexer_name': u'python',
            'extension_src': u'py',
            'extension_bin': u'py',
            'interpreter': '*ip'}
            },
        ],
    },
    ]


