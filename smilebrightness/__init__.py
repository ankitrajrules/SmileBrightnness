"""SmileBrightness: dim your screen when you stop smiling."""

from .config import Config
from .controller import DimController
from .detector import SmileDetector

__all__ = ["Config", "DimController", "SmileDetector"]
__version__ = "0.2.0"
