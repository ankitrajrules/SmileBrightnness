# SmileBrightness

SmileBrightness is a Python application that uses computer vision to detect smiles and automatically adjusts your screen brightness. When you smile, the screen stays at normal brightness; when you stop smiling, the screen dims after a short delay.

## Features

- Real-time face and smile detection using OpenCV
- Automatic screen brightness adjustment
- Configurable sensitivity and brightness levels
- Graceful cleanup on exit

## Requirements

- Python 3.x
- OpenCV (cv2)
- screen-brightness-control
- Webcam

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/SmileBrightness.git
cd SmileBrightness
```

2. Create a virtual environment and activate it:
```bash
python -m venv smile_env
# On Windows
smile_env\Scripts\activate
# On Unix or MacOS
source smile_env/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python main.py
```

- The application will start using your default webcam
- Your screen will maintain normal brightness when you smile
- The screen will dim after 30 frames without detecting a smile
- Press 'q' to quit the application

## Configuration

You can adjust the following parameters in `main.py`:
- `NO_SMILE_THRESHOLD`: Number of consecutive frames without a smile before dimming (default: 30)
- `LOWER_BRIGHTNESS`: Screen brightness level when not smiling (default: 30)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- OpenCV for their Haar Cascade Classifiers
- The screen-brightness-control package developers