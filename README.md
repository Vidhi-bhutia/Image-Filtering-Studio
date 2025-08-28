# Image Filter Studio

A modern Flask web application that allows users to upload images and apply a variety of filters and transformations in real time. Built with Flask and Pillow (PIL), this app provides a simple, beautiful interface for experimenting with image effects.

## Features

- **Upload Images:** Supports PNG, JPG, and WEBP formats (up to ~10MB recommended).
- **Image Filters:**
  - Grayscale
  - Blur (with adjustable strength)
  - Contour
  - Edge Enhance
- **Transformations:**
  - Rotate (0–359°)
  - Flip Horizontal / Vertical
  - Adjust Brightness (0.2–2.0)
  - Adjust Contrast (0.2–2.0)
- **Live Preview:** See the processed image instantly after applying filters.
- **Download Result:** Download the processed image with a single click.
- **Responsive UI:** Clean, modern design with CSS gradients and cards.

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository or extract the ZIP:**
   ```sh
   git clone https://github.com/Vidhi-bhutia/Image-Filtering-Studio.git
   cd Image-Filtering-Studio
   ```

2. **(Optional) Create a virtual environment:**
   ```sh
   python -m venv myenv
   # On Windows:
   myenv\Scripts\activate
   # On macOS/Linux:
   source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

### Running the App

```sh
# If using the virtual environment, ensure it's activated
python application.py
```

- The app will start on `http://127.0.0.1:5000/` by default.
- Open this URL in your browser to use the app.

#### Using Gunicorn (for production)
```sh
gunicorn -w 4 application:app
```

## Project Structure

```
application.py           # Main Flask app
requirements.txt         # Python dependencies
runtime.txt              # (Optional) Python runtime version for deployment
static/
|--- style.css              # App styles
templates/
|--- base.html              # Base template
|--- index.html             # Main page template
```

## How It Works

- The user uploads an image and selects desired filters/transformations.
- The Flask backend processes the image using Pillow (PIL) based on the selected options.
- The processed image is displayed for preview and can be downloaded.

## Customization

- **Add More Filters:**
  - Extend the filter dropdown in `templates/index.html`.
  - Add corresponding logic in `application.py` using Pillow.
- **Change UI:**
  - Edit `static/style.css` and the HTML templates in `templates/`.

## Dependencies
- Flask
- Pillow
- Gunicorn (for production)

*Built with Flask + Pillow. Enjoy experimenting with your images!*
