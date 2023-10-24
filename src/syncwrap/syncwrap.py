''' A library for wrapping sync functions in async coroutines. '''

# Standard library imports.
import asyncio


def syncwrap(asyncfunc):
    ''' Decorator to wrap a sync function and either run in the current
        event loop, or run in a new loop and wait for the result. '''

    if not asyncio.iscoroutinefunction(asyncfunc):
        # If the function is not a coroutine, just return it.
        return asyncfunc

    async def wrapper(*args, **kwargs):
        try:
            # will raise a RuntimeError if no loop is running
            loop = asyncio.get_running_loop()
            if loop.is_running():
                return await asyncfunc(*args, **kwargs)
            else:
                return await loop.run_until_complete(asyncfunc(*args, **kwargs))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            return await loop.run_until_complete(asyncfunc(*args, **kwargs))
    return wrapper
