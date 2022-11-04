from __future__ import annotations

from objects.type_hints import delegate, func


class Handle:
    def __init__(self):
        self.value: bool = False

    def __get__(self, instance, owner):
        return instance.value

    def __call__(self, *args, **kwargs):
        self.value = True


class Event:
    def __init__(self):
        self.delegate: delegate = set()

    def __add__(self, other: func) -> Event:
        self.delegate.add(other)
        return self

    def __sub__(self, other: func) -> Event:
        self.delegate.remove(other)
        return self

    def __call__(self, *args, **kwargs):
        for f in self.delegate:
            f(*args, **kwargs)
