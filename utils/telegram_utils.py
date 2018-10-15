from functools import wraps


def handler(app, handler_type, state=None, **options):
    def wrapper(func):
        new_handler = handler_type(callback=func, **options)
        new_handler.state = state
        app.handler_registry.append(new_handler)

        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped
    return wrapper
