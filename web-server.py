# app.py - Flask web server for the pulse oximeter

from flask import Flask, render_template, Response, jsonify
import base64
import time
from pulse_oximeter import PulseOximeter

app = Flask(__name__)
oximeter = PulseOximeter(buffer_size=150, fps=30)

@app.route('/')
def index():
    """Serve the index page"""
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_monitoring():
    """Start the pulse oximeter monitoring"""
    success = oximeter.start_monitoring()
    return jsonify({'success': success})

@app.route('/api/stop', methods=['POST'])
def stop_monitoring():
    """Stop the pulse oximeter monitoring"""
    success = oximeter.stop_monitoring()
    return jsonify({'success': success})

@app.route('/api/data')
def get_data():
    """Get current pulse and SpO2 data"""
    data = oximeter.get_current_data()
    
    # Convert ROI image to base64 for HTML display
    if 'roi_image' in data:
        data['roi_image'] = base64.b64encode(data['roi_image']).decode('utf-8')
    
    return jsonify(data)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8000, threaded=True)
    finally:
        # Ensure camera is released when app is closed
        oximeter.stop_monitoring()
