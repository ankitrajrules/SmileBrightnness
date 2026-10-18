import numpy as np
import pytest

from smilebrightness.config import Config
from smilebrightness.detector import SmileDetector


def test_blank_frame_is_not_a_smile():
    frame = np.zeros((240, 320, 3), dtype=np.uint8)
    assert SmileDetector().detect(frame) is False


def test_annotate_does_not_crash_on_noise():
    rng = np.random.default_rng(0)
    frame = rng.integers(0, 255, (240, 320, 3), dtype=np.uint8)
    assert isinstance(SmileDetector().detect(frame, annotate=True), bool)


@pytest.mark.parametrize(
    "kwargs",
    [{"dim_level": 101}, {"dim_level": -1}, {"dim_after_seconds": -1}, {"frame_interval": 0}],
)
def test_config_rejects_bad_values(kwargs):
    with pytest.raises(ValueError):
        Config(**kwargs)
