"""Face + smile detection using OpenCV Haar cascades."""

from __future__ import annotations

import cv2
import numpy as np

from .config import Config


class SmileDetector:
    """Detects whether anyone in a frame is smiling."""

    def __init__(self, config: Config | None = None) -> None:
        self.config = config or Config()
        face_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        smile_path = cv2.data.haarcascades + "haarcascade_smile.xml"
        self._face = cv2.CascadeClassifier(face_path)
        self._smile = cv2.CascadeClassifier(smile_path)
        if self._face.empty() or self._smile.empty():
            raise RuntimeError("Could not load OpenCV Haar cascade files")

    def detect(self, frame: np.ndarray, annotate: bool = False) -> bool:
        """Return True if any detected face is smiling.

        With annotate=True, boxes are drawn on `frame` in place (blue for
        faces, green for smiles) for the preview window.
        """
        cfg = self.config
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self._face.detectMultiScale(
            gray,
            scaleFactor=cfg.face_scale_factor,
            minNeighbors=cfg.face_min_neighbors,
            minSize=cfg.face_min_size,
        )

        smiling = False
        for x, y, w, h in faces:
            if annotate:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            smiles = self._smile.detectMultiScale(
                gray[y : y + h, x : x + w],
                scaleFactor=cfg.smile_scale_factor,
                minNeighbors=cfg.smile_min_neighbors,
                minSize=cfg.smile_min_size,
            )
            if len(smiles) > 0:
                smiling = True
                if annotate:
                    for sx, sy, sw, sh in smiles:
                        cv2.rectangle(
                            frame, (x + sx, y + sy), (x + sx + sw, y + sy + sh), (0, 255, 0), 2
                        )
        return smiling
