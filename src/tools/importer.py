def importer(name, root_package=False, relative_globals=None, level=0):

    """ We only import modules, functions can be looked up on the module.
    Usage: 

    from foo.bar import baz
    baz = importer('foo.bar.baz')

    import foo.bar.baz
    foo = importer('foo.bar.baz', root_package=True)
    foo.bar.baz

    from .. import baz (level = number of dots)
    baz = importer('baz', relative_globals=globals(), level=2)
    """
    return __import__(name, locals=None, # locals has no use
                      globals=relative_globals, 
                      fromlist=[] if root_package else [None],
                      level=level)