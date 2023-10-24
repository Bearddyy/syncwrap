

def test_import_syncwrap():
    from syncwrap import syncwrap
    assert syncwrap

def test_has_decorator():
    from syncwrap import syncwrap
    assert hasattr(syncwrap, 'syncwrap')