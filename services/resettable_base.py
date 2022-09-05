from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Callable


class ResettableBase(ABC):
    """Baseclass for all services that need to be reset."""

    def __init__(self, daily: bool, interval: int) -> None:
        super().__init__()
        self.updated = datetime.now()
        self.daily = daily
        self.interval = interval

    def reset_dispatch(self) -> None:
        """Checks wether a reset is necessary or not and calls it if so."""
        if self.daily and self.updated.day != datetime.now().day:
            self.reset()
            return
        if not self.daily and (datetime.now() - self.updated).seconds > self.interval:
            self.reset()
            return

    @abstractmethod
    def reset(self) -> None:
        """Forces implementation of this method in all children."""
        ...


def depends_on_reset(fun: Callable[[ResettableBase, Any], Any]) -> Callable[[ResettableBase, Any], Any]:
    """Decorator used to decorate any method within a derived class of 'ResettableBase'.

    Extends the decorated function with a reset check before the actual function is called.
    """

    def wrapper(self: ResettableBase, *args, **kwargs):
        self.reset_dispatch()
        return fun(self, *args, **kwargs)

    return wrapper
