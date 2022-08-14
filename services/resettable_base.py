from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Callable


class ResettableBase(ABC):
    def __init__(self, daily: bool, interval: int) -> None:
        super().__init__()
        self.updated = datetime.now()
        self.daily = daily
        self.interval = interval

    def reset_dispatch(self) -> None:
        if self.daily and self.updated.day != datetime.now().day:
            self.reset()
            return
        if not self.daily and (datetime.now() - self.updated).seconds > self.interval:
            self.reset()
            return

    @abstractmethod
    def reset(self) -> None:
        ...


def depends_on_reset(fun: Callable[[ResettableBase, Any], Any]) -> Callable[[ResettableBase, Any], Any]:
    def wrapper(self: ResettableBase, *args, **kwargs):
        self.reset_dispatch()
        return fun(self, *args, **kwargs)

    return wrapper
