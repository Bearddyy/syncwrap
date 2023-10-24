''' A library for wrapping sync functions in async coroutines. '''

# Standard library imports.
import asyncio

def syncwrap(asyncfunc=None, timeout=None):
    ''' Decorator to wrap a sync function and either run in the current
        event loop, or run in a new loop and wait for the result.
        optional timeout parameter to wait for the result.
    '''
    # Note: nested decorator function is required to pass parameters like timeout.
    def _syncwrap(asyncfunc):
        if not asyncio.iscoroutinefunction(asyncfunc):
            # If the function is not a coroutine, just return it.
            return asyncfunc

        async def wrapper(*args, **kwargs):
            try:
                # will raise a RuntimeError if no loop is running
                loop = asyncio.get_running_loop()
                if loop.is_running():
                    return await asyncio.wait_for(asyncfunc(*args, **kwargs), timeout)
                else:
                    if timeout:
                        return await asyncio.wait_for(asyncfunc(*args, **kwargs), timeout)
                    else:
                        return await loop.run_until_complete(asyncfunc(*args, **kwargs))
            except RuntimeError:
                loop = asyncio.new_event_loop()
                if timeout:
                    return await asyncio.wait_for(asyncfunc(*args, **kwargs), timeout)
                else:
                    return await loop.run_until_complete(asyncfunc(*args, **kwargs))
        return wrapper
    if asyncfunc is None:
        return _syncwrap
    else:
        return _syncwrap(asyncfunc)
