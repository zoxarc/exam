from __future__ import annotations

from objects.type_hints import delegate, func


class Event:
    def __init__(self):
        # type hints
        self.delegate: delegate

        #
        self.delegate = set()

    def __add__(self, other: func) -> Event:
        self.delegate.add(other)
        return self

    def __sub__(self, other: func) -> Event:
        self.delegate.remove(other)
        return self

    def __call__(self, *args, **kwargs):
        for f in self.delegate:
            f(*args, **kwargs)
