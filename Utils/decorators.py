from MiniGames.Utils.exceptions import AccessException

__IS_HIDDEN__ = True


def inner_method(method):
    def inner(*args, **kwargs):
        if __IS_HIDDEN__:
            raise AccessException("You should not be accessing this method. Checkout events in readme.md")
        method(*args, **kwargs)

    return inner
