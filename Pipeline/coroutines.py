import typing


class WaitFor:
    def should_call(self, delta_time: float) -> bool:
        raise NotImplementedError()


class WaitForSeconds(WaitFor):
    def __init__(self, amount):
        self.__amount = amount

    def should_call(self, delta_time):
        self.__amount -= delta_time
        return self.__amount <= 0


class WaitForEndOfFrame(WaitFor):
    def should_call(self, delta_time):
        return True


class WaitForEndOfFrames(WaitFor):
    def __init__(self, n_frames):
        self.__frames = n_frames

    def should_call(self, delta_time):
        self.__frames -= 1
        return self.__frames <= 0


class WaitWhileTrue(WaitFor):
    def __init__(self, func: typing.Callable[[], bool]):
        self.__func = func

    def should_call(self, delta_time):
        return not self.__func()


class WaitWhileFalse(WaitFor):
    def __init__(self, func: typing.Callable[[], bool]):
        self.__func = func

    def should_call(self, delta_time):
        return self.__func()

