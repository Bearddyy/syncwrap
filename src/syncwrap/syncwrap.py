''' A library for wrapping sync functions in async coroutines. '''

# Standard library imports.
import asyncio


def syncwrap(func):
    ''' Decorator to wrap a sync function and either run in the current
        event loop, or run in a new thread and wait for the result. '''
    return func