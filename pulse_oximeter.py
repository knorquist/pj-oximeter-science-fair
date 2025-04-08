# pulse_oximeter.py - Main pulse oximeter implementation

import numpy as np
import time
from collections import deque
import threading
import json
import cv2
from picamera2 import Picamera2

class PulseOximeter:
    def __init__(self, buffer_size=100, fps=30):
        self.buffer_size = buffer_size
        self.data_buffer_red = deque(maxlen=buffer_size)
        self.data_buffer_ir = deque(maxlen=buffer_size)
        self.times = deque(maxlen=buffer_size)
        self.pulse_rate = 0
        self.spo2 = 0
        self.frame = None
        self.roi = None
        self.running = False
        self.lock = threading.Lock()
        self.fps = fps
        self.camera = None
        
    def start_camera(self):
        """Initialize the Raspberry Pi camera using picamera2"""
        try:
            self.camera = Picamera2()
            # Configure camera with 640x480 resolution
            config = self.camera.create_still_configuration(
                main={"size": (640, 480)},
                controls={"FrameDurationLimits": (int(1000000/self.fps), 100000000)}
            )
            self.camera.configure(config)
            self.camera.start()
            time.sleep(1)  # Give camera time to initialize
            return True
        except Exception as e:
            print(f"Camera initialization error: {e}")
            return False
    
    def stop_camera(self):
        """Release the camera resource"""
        if self.camera is not None:
            self.camera.stop()
            self.camera.close()
            self.camera = None
    
    def start_monitoring(self):
        """Start the monitoring thread"""
        if not self.running:
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_worker)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            return True
        return False
    
    def stop_monitoring(self):
        """Stop the monitoring thread"""
        self.running = False
        if hasattr(self, 'monitoring_thread'):
            self.monitoring_thread.join(timeout=1.0)
        self.stop_camera()
        return True
    
    def _monitoring_worker(self):
        """Worker thread for monitoring pulse and SpO2"""
        if not self.start_camera():
            print("Failed to open camera")
            self.running = False
            return
        
        while self.running:
            try:
                # Capture frame using picamera2
                self.frame = self.camera.capture_array()
                
                # Extract ROI (assumed to be center of frame)
                height, width = self.frame.shape[:2]
                roi_size = min(width, height) // 3
                roi_x = (width - roi_size) // 2
                roi_y = (height - roi_size) // 2
                self.roi = self.frame[roi_y:roi_y+roi_size, roi_x:roi_x+roi_size]
                
                # Process frame
                self._process_frame()
                
                # Sleep to maintain frame rate
                time.sleep(1.0/self.fps)
            except Exception as e:
                print(f"Error in monitoring thread: {e}")
                time.sleep(0.5)  # Short delay before retry
    
    def _process_frame(self):
        """Process a video frame to extract pulse and SpO2 data"""
        if self.roi is None:
            return
        
        # Extract average color from ROI
        mean_bgr = cv2.mean(self.roi)
        # Red and IR approximation (we're using visible light only but treating red as "red" and blue as "IR" for simulation)
        red_val = mean_bgr[2]  # Red channel
        ir_val = mean_bgr[0]   # Blue channel (as IR approximation)
        
        current_time = time.time()
        
        with self.lock:
            # Add data to buffers
            self.data_buffer_red.append(red_val)
            self.data_buffer_ir.append(ir_val)
            self.times.append(current_time)
            
            # Process data if we have enough samples
            if len(self.data_buffer_red) >= self.buffer_size // 2:
                self._calculate_vitals()
    
    def _calculate_vitals(self):
        """Calculate pulse rate and SpO2 from buffered data"""
        # Convert to numpy arrays for processing
        red_data = np.array(self.data_buffer_red)
        ir_data = np.array(self.data_buffer_ir)
        times = np.array(self.times)
        
        # Apply bandpass filter (simplified as moving average here)
        red_data_filtered = self._moving_average(red_data, 5)
        ir_data_filtered = self._moving_average(ir_data, 5)
        
        # Calculate pulse rate (simplified method using zero-crossings)
        if len(times) > 1:
            # Normalize signals
            red_normalized = (red_data_filtered - np.mean(red_data_filtered)) / np.std(red_data_filtered)
            
            # Count zero crossings to estimate frequency
            zero_crossings = np.where(np.diff(np.signbit(red_normalized)))[0]
            if len(zero_crossings) > 1:
                # Time between zero crossings
                time_diff = times[-1] - times[0]
                # Approximate beats per minute
                if time_diff > 0:
                    beats_per_sec = len(zero_crossings) / (2 * time_diff)
                    self.pulse_rate = int(beats_per_sec * 60)
                    # Constrain to reasonable values (40-180 BPM)
                    self.pulse_rate = max(40, min(180, self.pulse_rate))
            
            # Calculate SpO2 (simplified formula)
            # Normally uses the ratio of ratios of red/IR absorption
            ac_red = np.std(red_data_filtered)
            dc_red = np.mean(red_data_filtered)
            ac_ir = np.std(ir_data_filtered)
            dc_ir = np.mean(ir_data_filtered)
            
            if dc_red > 0 and dc_ir > 0:
                ratio = (ac_red / dc_red) / (ac_ir / dc_ir)
                # Simplified SpO2 calculation (would need calibration in real device)
                self.spo2 = int(110 - 25 * ratio)
                # Constrain to reasonable values (70-100%)
                self.spo2 = max(70, min(100, self.spo2))
    
    def _moving_average(self, data, window_size):
        """Apply simple moving average filter"""
        return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    
    def get_current_data(self):
        """Get the current pulse rate, SpO2 and ROI image"""
        with self.lock:
            result = {
                'pulse_rate': self.pulse_rate,
                'spo2': self.spo2,
                'timestamp': time.time()
            }
            
            # Get historical data for graphing
            if len(self.data_buffer_red) > 0:
                result['historical_data'] = {
                    'red': list(self.data_buffer_red),
                    'ir': list(self.data_buffer_ir),
                    'times': [t - self.times[0] if self.times else 0 for t in self.times]
                }
            
            # Encode ROI as JPEG for web display
            if self.roi is not None:
                ret, jpeg = cv2.imencode('.jpg', self.roi)
                if ret:
                    result['roi_image'] = jpeg.tobytes()
            
            return result