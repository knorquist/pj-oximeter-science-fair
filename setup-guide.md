# Raspberry Pi Pulse Oximeter Setup Guide for Bookworm

This guide will help you set up a DIY pulse oximeter using a Raspberry Pi Zero W and a Raspberry Pi Camera Module on Raspberry Pi OS Bookworm.

## Hardware Requirements

1. Raspberry Pi Zero W (with Wi-Fi)
2. Raspberry Pi Camera Module v2.1
3. Camera adapter cable for Pi Zero (the Pi Zero uses a smaller camera connector)
4. MicroSD card (8GB or larger)
5. Power supply for Raspberry Pi
6. Optional: Small case or enclosure

## Software Setup

### 1. Set up Raspberry Pi OS Bookworm

1. Flash Raspberry Pi OS Bookworm (Lite or Desktop) to your MicroSD card using the Raspberry Pi Imager.
2. Configure Wi-Fi and SSH during the flashing process.
3. Boot your Raspberry Pi and connect via SSH or monitor.

### 2. Camera Connection

The Raspberry Pi Zero W has a connector labeled "TV" which is actually the Camera Serial Interface (CSI) port, despite the confusing label. To connect the camera:

1. Power off your Raspberry Pi completely
2. Use the special ribbon cable designed for the Pi Zero (narrower than standard camera cable)
3. The blue side of the ribbon should face away from the board (toward the "TV" text)
4. Gently lift the black plastic clip on the connector, insert the cable fully, and press the clip back down

### 3. Install Required Packages

Update your system first:

```bash
sudo apt update
sudo apt upgrade -y
```

Install the required packages for our pulse oximeter:

```bash
sudo apt install -y python3-pip python3-picamera2 python3-opencv python3-flask libcamera-apps
```

### 4. Test the Camera

First, verify the camera is working:

```bash
libcamera-hello
```

This should show a preview from the camera for 5 seconds. If this works, your camera is properly connected.

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