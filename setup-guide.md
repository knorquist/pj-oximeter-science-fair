# Raspberry Pi Pulse Oximeter Setup Guide

This guide will help you set up a DIY pulse oximeter using a Raspberry Pi Zero and a Raspberry Pi Camera Module.

## Hardware Requirements

1. Raspberry Pi Zero W (with Wi-Fi)
2. Raspberry Pi Camera Module
3. MicroSD card (8GB or larger)
4. Power supply for Raspberry Pi
5. Optional: Small case or enclosure

## Software Setup

### 1. Set up Raspberry Pi OS

1. Flash Raspberry Pi OS (Lite or Desktop) to your MicroSD card using the Raspberry Pi Imager.
2. Configure Wi-Fi and SSH during the flashing process.
3. Boot your Raspberry Pi and connect via SSH or monitor.

### 2. Install Required Packages

Update your system first:

```bash
sudo apt update
sudo apt upgrade -y
```

Install dependencies for OpenCV and other libraries:

```bash
sudo apt install -y python3-pip python3-venv libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libatlas-base-dev gfortran
```

### 3. Enable Camera Module

1. Run `sudo raspi-config`
2. Navigate to "Interface Options" → "Camera"
3. Enable the camera module
4. Reboot the Raspberry Pi: `sudo reboot`

### 4. Set Up Python Environment

Create a virtual environment and install requirements:

```bash
mkdir ~/pulse-oximeter
cd ~/pulse-oximeter

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Create project files
# (Copy the provided Python, Flask, and HTML files here)

# Install required packages
pip install -r requirements.txt
```

## Project Structure

Ensure your project has the following file structure:

```
pulse-oximeter/
├── pulse_oximeter.py
├── app.py
├── requirements.txt
└── templates/
    └── index.html
```

## Running the Application

1. Make sure your Raspberry Pi Camera is properly connected.
2. Navigate to your project directory:
   ```bash
   cd ~/pulse-oximeter
   source venv/bin/activate
   ```
3. Start the web server:
   ```bash
   python app.py
   ```
4. Open a web browser and navigate to `http://[Raspberry_Pi_IP]:8000`

## Usage Instructions

1. Place your fingertip gently on the camera lens. Cover it completely but don't press too hard.
2. For best results, ensure:
   - Your finger covers the entire camera lens
   - You have good lighting conditions (not too bright or dark)
   - Your finger remains still during measurement
3. Click the "Start Monitoring" button on the web interface.
4. The application will display:
   - Your pulse rate in BPM (beats per minute)
   - Your SpO₂ level (blood oxygen saturation) in percentage
   - A real-time graph of the detected signals
5. Click "Stop Monitoring" when finished.

## Troubleshooting

- **No camera image**: Check that the camera is properly connected and enabled in raspi-config.
- **Inaccurate readings**: Try adjusting the position of your finger, the lighting conditions, or reduce motion.
- **Web interface not loading**: Verify the server is running and check your IP address and firewall settings.
- **Low performance**: Consider closing other applications on the Raspberry Pi or reducing the framerate in the code.

## Limitations

This DIY pulse oximeter is for educational purposes only and should not be used for medical diagnosis. The accuracy will be significantly lower than medical-grade pulse oximeters for several reasons:

1. Medical devices use specific wavelengths of light (red and infrared LEDs)
2. Consumer cameras have filters that affect the detection of these wavelengths
3. The algorithm used here is simplified compared to medical devices
4. There's no clinical calibration of the measurements

## Further Improvements

- Add a red LED to improve blood oxygen detection
- Implement more sophisticated signal processing algorithms
- Add data logging capabilities
- Create a mobile app interface
- Add user accounts to track measurements over time
