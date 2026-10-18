"""Pure dim/restore decision logic, with no OpenCV and no hardware.

Keeping this separate from the camera loop means it can be unit tested with
fake timestamps, and it only asks for a brightness change when the state
actually flips (the original script re-sent the same value on every frame).
"""

from __future__ import annotations


class DimController:
    """Decides when to dim the screen and when to restore it."""

    def __init__(self, restore_level: int, dim_level: int, dim_after_seconds: float) -> None:
        self.restore_level = restore_level
        self.dim_level = dim_level
        self.dim_after_seconds = dim_after_seconds
        self._dimmed = False
        self._last_smile: float | None = None

    @property
    def dimmed(self) -> bool:
        return self._dimmed

    def update(self, smiling: bool, now: float) -> int | None:
        """Feed one observation. Returns a brightness level to apply, or None.

        The first observation starts the "no smile" clock, so the screen never
        dims the instant the program launches.
        """
        if self._last_smile is None:
            self._last_smile = now

        if smiling:
            self._last_smile = now
            if self._dimmed:
                self._dimmed = False
                return self.restore_level
            return None

        if not self._dimmed and now - self._last_smile >= self.dim_after_seconds:
            self._dimmed = True
            return self.dim_level
        return None
