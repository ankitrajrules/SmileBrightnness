"""Tunable settings, kept in one place so the CLI and tests share them."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    # Behaviour
    dim_after_seconds: float = 5.0  # no smile for this long -> dim the screen
    dim_level: int = 30  # brightness (0-100) while dimmed
    frame_interval: float = 0.2  # seconds between webcam samples
    camera_index: int = 0
    preview: bool = True  # show the annotated webcam window

    # Haar cascade tuning (see the OpenCV docs for detectMultiScale)
    face_scale_factor: float = 1.3
    face_min_neighbors: int = 5
    face_min_size: tuple[int, int] = (30, 30)
    smile_scale_factor: float = 1.8
    smile_min_neighbors: int = 20
    smile_min_size: tuple[int, int] = (25, 25)

    def __post_init__(self) -> None:
        if not 0 <= self.dim_level <= 100:
            raise ValueError("dim_level must be between 0 and 100")
        if self.dim_after_seconds < 0:
            raise ValueError("dim_after_seconds must be >= 0")
        if self.frame_interval <= 0:
            raise ValueError("frame_interval must be > 0")
