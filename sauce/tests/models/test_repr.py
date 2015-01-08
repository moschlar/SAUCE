'''
Created on Apr 16, 2014

@author: moschlar
'''

from sauce import model

entities = [x for x in model.__dict__.itervalues()
    if isinstance(x, type) and issubclass(x, model.DeclarativeBase)]


def _test_repr(entity):
    print repr(entity())


def test_repr():
    for entity in entities:
        yield _test_repr, entity
