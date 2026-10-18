# SmileBrightness

[![CI](https://github.com/ankitrajrules/SmileBrightnness/actions/workflows/ci.yml/badge.svg)](https://github.com/ankitrajrules/SmileBrightnness/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Dims your screen when you stop smiling. A small Python tool that watches your webcam with OpenCV, and restores your brightness the moment you smile again.

It started as a joke, but it's a compact example of a real-time vision loop with clean separation between **detection**, **decision logic** and **side effects**, which is what makes it testable.

## How it works

```
webcam frame ──> SmileDetector ──> smiling? ──> DimController ──> brightness change (or None)
 (OpenCV)        (Haar cascades)               (pure logic)        (screen-brightness-control)
```

- **`detector.py`** finds faces, then looks for a smile inside each face region.
- **`controller.py`** is a small state machine: no smile for `--dim-after` seconds means dim; a smile means restore. It only requests a brightness change when the state flips, so it doesn't hammer your display driver every frame. It has no OpenCV or hardware dependency, so it's unit-tested with fake timestamps.
- **`cli.py`** wires it together and always restores your original brightness on exit, even on Ctrl+C or a camera error.

Video frames are processed locally and never saved or sent anywhere.

## Install

```bash
git clone https://github.com/ankitrajrules/SmileBrightnness.git
cd SmileBrightnness
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

## Usage

```bash
smilebrightness                  # or: python -m smilebrightness
smilebrightness --dim-after 10 --dim-level 20
smilebrightness --no-preview -v  # headless, log brightness changes
```

| Flag | Default | Meaning |
|---|---|---|
| `--dim-after SECONDS` | `5` | Time without a smile before dimming |
| `--dim-level 0-100` | `30` | Brightness while dimmed |
| `--interval SECONDS` | `0.2` | Time between webcam samples |
| `--camera INDEX` | `0` | Which webcam to use |
| `--no-preview` | off | No window; stop with Ctrl+C |
| `-v, --verbose` | off | Log each brightness change |

With the preview window open, press `q` to quit. Faces are boxed in blue and smiles in green.

## Platform support

Brightness control is provided by [screen-brightness-control](https://github.com/Crozzers/screen_brightness_control), so support follows that library (Windows and Linux). Some external monitors need DDC/CI enabled.

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

CI runs lint and tests on Python 3.10 to 3.12 using headless OpenCV, so no camera or display is needed.

## Known limitations

- Haar cascades are fast and dependency-light but sensitive to lighting and head angle, so expect some false positives and misses. Tune `smile_min_neighbors` in `config.py` if needed.
- Only the first monitor's brightness is read as the "original" level.
- OpenCV is pinned to the 4.x line because 5.x removed `cv2.CascadeClassifier`. Moving to a landmark-based detector (see roadmap) would lift this.

## Roadmap

- [ ] Swap Haar cascades for a landmark-based detector (e.g. MediaPipe) for better accuracy
- [ ] Smooth detections over a short window to reduce flicker
- [ ] System tray app with pause/resume

## License

MIT, see [LICENSE](LICENSE).
