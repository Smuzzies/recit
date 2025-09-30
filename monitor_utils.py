#!/usr/bin/env python3
"""
Monitor detection and resolution utilities
"""

import subprocess
import re
from typing import List, Tuple, Dict, Optional

class Monitor:
    def __init__(self, name: str, width: int, height: int, x: int = 0, y: int = 0, is_primary: bool = False):
        self.name = name
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.is_primary = is_primary
        
    @property
    def resolution(self) -> str:
        return f"{self.width}x{self.height}"
    
    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height
    
    @property
    def aspect_ratio_string(self) -> str:
        ratio = self.aspect_ratio
        if abs(ratio - 16/9) < 0.1:
            return "16:9"
        elif abs(ratio - 21/9) < 0.1:
            return "21:9"
        elif abs(ratio - 32/9) < 0.1:
            return "32:9"
        elif abs(ratio - 4/3) < 0.1:
            return "4:3"
        else:
            return f"{ratio:.2f}:1"
    
    def __str__(self):
        primary = " (Primary)" if self.is_primary else ""
        return f"{self.name}: {self.resolution} ({self.aspect_ratio_string}){primary}"

class MonitorDetector:
    def __init__(self):
        self.monitors: List[Monitor] = []
        self.detect_monitors()
    
    def detect_monitors(self):
        """Detect connected monitors using xrandr"""
        self.monitors = []
        
        try:
            result = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
            if result.returncode != 0:
                # Fallback to basic detection
                self._detect_fallback()
                return
            
            output = result.stdout
            
            # Parse xrandr output
            for line in output.split('\n'):
                if ' connected' in line:
                    self._parse_monitor_line(line)
                    
        except FileNotFoundError:
            # xrandr not available, use fallback
            self._detect_fallback()
    
    def _parse_monitor_line(self, line: str):
        """Parse a single monitor line from xrandr output"""
        parts = line.split()
        if len(parts) < 3:
            return
            
        monitor_name = parts[0]
        is_primary = 'primary' in line
        
        # Look for resolution pattern like "1920x1080+0+0"
        resolution_match = re.search(r'(\d+)x(\d+)\+(\d+)\+(\d+)', line)
        if resolution_match:
            width = int(resolution_match.group(1))
            height = int(resolution_match.group(2))
            x = int(resolution_match.group(3))
            y = int(resolution_match.group(4))
            
            monitor = Monitor(monitor_name, width, height, x, y, is_primary)
            self.monitors.append(monitor)
    
    def _detect_fallback(self):
        """Fallback monitor detection using xdpyinfo"""
        try:
            result = subprocess.run(['xdpyinfo'], capture_output=True, text=True)
            if result.returncode == 0:
                output = result.stdout
                
                # Look for dimensions
                match = re.search(r'dimensions:\s+(\d+)x(\d+)', output)
                if match:
                    width = int(match.group(1))
                    height = int(match.group(2))
                    
                    monitor = Monitor("Screen", width, height, 0, 0, True)
                    self.monitors.append(monitor)
                    return
        except FileNotFoundError:
            pass
        
        # Ultimate fallback - common resolutions
        monitor = Monitor("Default", 1920, 1080, 0, 0, True)
        self.monitors.append(monitor)
    
    def get_primary_monitor(self) -> Optional[Monitor]:
        """Get the primary monitor"""
        for monitor in self.monitors:
            if monitor.is_primary:
                return monitor
        
        # If no primary found, return first monitor
        return self.monitors[0] if self.monitors else None
    
    def get_total_screen_size(self) -> Tuple[int, int]:
        """Get total screen dimensions across all monitors"""
        if not self.monitors:
            return (1920, 1080)
        
        max_x = max(monitor.x + monitor.width for monitor in self.monitors)
        max_y = max(monitor.y + monitor.height for monitor in self.monitors)
        
        return (max_x, max_y)
    
    def calculate_scaled_dimensions(self, monitor: Monitor, target_height: int) -> Tuple[int, int]:
        """Calculate scaled dimensions maintaining aspect ratio"""
        aspect_ratio = monitor.aspect_ratio
        width = int(target_height * aspect_ratio)
        
        # Ensure even numbers (required by some codecs)
        if width % 2 != 0:
            width += 1
        if target_height % 2 != 0:
            target_height += 1
            
        return (width, target_height)
    
    def estimate_file_size(self, monitor: Monitor, target_height: int, fps: int, duration_seconds: int = 60, format_type: str = 'webm') -> str:
        """Estimate file size for given settings"""
        width, height = self.calculate_scaled_dimensions(monitor, target_height)
        
        # Rough estimates based on typical encoding
        if format_type == 'webm':
            # VP9 encoding
            if target_height <= 480:
                bitrate_mbps = 0.5
            elif target_height <= 720:
                bitrate_mbps = 1.0
            else:
                bitrate_mbps = 2.0
        else:  # mp4
            # H.264 encoding
            if target_height <= 480:
                bitrate_mbps = 1.0
            elif target_height <= 720:
                bitrate_mbps = 2.5
            else:
                bitrate_mbps = 5.0
        
        # Calculate file size
        file_size_mb = (bitrate_mbps * duration_seconds) / 8  # Convert bits to bytes
        
        if file_size_mb < 1:
            return f"{file_size_mb * 1024:.0f} KB"
        elif file_size_mb < 1024:
            return f"{file_size_mb:.1f} MB"
        else:
            return f"{file_size_mb / 1024:.1f} GB"

def main():
    """Test monitor detection"""
    detector = MonitorDetector()
    
    print("🖥️  Detected Monitors:")
    print("=" * 40)
    
    for i, monitor in enumerate(detector.monitors, 1):
        print(f"{i}. {monitor}")
        
        # Show scaled dimensions
        for height in [480, 720, 1080]:
            width, h = detector.calculate_scaled_dimensions(monitor, height)
            size_estimate = detector.estimate_file_size(monitor, height, 30, 60)
            print(f"   {height}p: {width}x{h} (~{size_estimate}/min)")
        print()
    
    primary = detector.get_primary_monitor()
    if primary:
        print(f"Primary monitor: {primary}")
    
    total_w, total_h = detector.get_total_screen_size()
    print(f"Total screen area: {total_w}x{total_h}")

if __name__ == "__main__":
    main()