"""Command-line entry point: webcam loop wiring detector -> controller -> display."""

from __future__ import annotations

import argparse
import logging
import time

import cv2

from .config import Config
from .controller import DimController
from .detector import SmileDetector

log = logging.getLogger("smilebrightness")


def _read_brightness() -> int:
    import screen_brightness_control as sbc

    value = sbc.get_brightness()
    return int(value[0] if isinstance(value, list) else value)


def _set_brightness(level: int) -> None:
    import screen_brightness_control as sbc

    sbc.set_brightness(level)


def build_parser() -> argparse.ArgumentParser:
    d = Config()
    p = argparse.ArgumentParser(
        prog="smilebrightness",
        description="Dim your screen when you stop smiling.",
    )
    p.add_argument("--dim-after", type=float, default=d.dim_after_seconds, metavar="SECONDS",
                   help="seconds without a smile before dimming (default: %(default)s)")
    p.add_argument("--dim-level", type=int, default=d.dim_level, metavar="0-100",
                   help="brightness while dimmed (default: %(default)s)")
    p.add_argument("--interval", type=float, default=d.frame_interval, metavar="SECONDS",
                   help="seconds between webcam samples (default: %(default)s)")
    p.add_argument("--camera", type=int, default=d.camera_index, metavar="INDEX",
                   help="webcam index (default: %(default)s)")
    p.add_argument("--no-preview", action="store_true",
                   help="run without the webcam window (stop with Ctrl+C)")
    p.add_argument("-v", "--verbose", action="store_true", help="log brightness changes")
    return p


def run(config: Config) -> int:
    detector = SmileDetector(config)
    original = _read_brightness()
    controller = DimController(original, config.dim_level, config.dim_after_seconds)

    cap = cv2.VideoCapture(config.camera_index)
    if not cap.isOpened():
        log.error("Could not open camera %d", config.camera_index)
        return 1

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                log.error("Lost the camera feed")
                return 1

            smiling = detector.detect(frame, annotate=config.preview)
            change = controller.update(smiling, time.monotonic())
            if change is not None:
                _set_brightness(change)
                log.info("brightness -> %d%%", change)

            if config.preview:
                cv2.imshow("SmileBrightness (q to quit)", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            time.sleep(config.frame_interval)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        _set_brightness(original)  # always leave the screen how we found it
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(message)s")
    try:
        config = Config(
            dim_after_seconds=args.dim_after,
            dim_level=args.dim_level,
            frame_interval=args.interval,
            camera_index=args.camera,
            preview=not args.no_preview,
        )
    except ValueError as exc:
        build_parser().error(str(exc))
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
