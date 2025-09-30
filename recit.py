#!/usr/bin/env python3
"""
Recit - A Beautiful Terminal Screen Recorder
Record your screen with style using a modern TUI interface.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static, Label
from textual.reactive import reactive
from textual.theme import Theme
import subprocess
import os
import signal
import time
from pathlib import Path
from datetime import datetime
import threading
import json

# Base2Tone Evening Theme
BASE2TONE_EVENING = Theme(
    name="base2tone-evening",
    primary="#6a51e6",
    secondary="#b37537",
    warning="#ffa142",
    error="#cb823a",
    success="#8a75f5",
    accent="#9a86fd",
    dark=True,
    variables={
        "background": "#2a2734",
        "surface": "#363342",
        "panel": "#545167",
        "boost": "#6c6783",
        "dark": "#2a2734",
        "foreground": "#bab8c7",
        "primary": "#6a51e6",
        "secondary": "#b37537",
        "accent": "#9a86fd",
        "warning": "#ffa142",
        "error": "#cb823a",
        "success": "#8a75f5",
    }
)

# Base2Tone Sea Theme
BASE2TONE_SEA = Theme(
    name="base2tone-sea",
    primary="#1d8991",
    secondary="#c44c00",
    warning="#ee8931",
    error="#d6490d",
    success="#1ca4ad",
    accent="#22b4be",
    dark=True,
    variables={
        "background": "#1d262f",
        "surface": "#28323d",
        "panel": "#475863",
        "boost": "#617481",
        "dark": "#1d262f",
        "foreground": "#a7b9c5",
        "primary": "#1d8991",
        "secondary": "#c44c00",
        "accent": "#22b4be",
        "warning": "#ee8931",
        "error": "#d6490d",
        "success": "#1ca4ad",
    }
)

# Base2Tone Forest Theme
BASE2TONE_FOREST = Theme(
    name="base2tone-forest",
    primary="#687d68",
    secondary="#d88011",
    warning="#f09000",
    error="#cf7800",
    success="#8fae8f",
    accent="#b3d6b3",
    dark=True,
    variables={
        "background": "#2a2d2a",
        "surface": "#353b35",
        "panel": "#485148",
        "boost": "#5e6e5e",
        "dark": "#2a2d2a",
        "foreground": "#b8c7b8",
        "primary": "#687d68",
        "secondary": "#d88011",
        "accent": "#b3d6b3",
        "warning": "#f09000",
        "error": "#cf7800",
        "success": "#8fae8f",
    }
)

# Base2Tone Field Theme
BASE2TONE_FIELD = Theme(
    name="base2tone-field",
    primary="#037764",
    secondary="#d4561e",
    warning="#e8863a",
    error="#c94a16",
    success="#0fbda0",
    accent="#25d0b4",
    dark=True,
    variables={
        "background": "#18201e",
        "surface": "#242e2c",
        "panel": "#42524f",
        "boost": "#667a77",
        "dark": "#18201e",
        "foreground": "#a4b7b4",
        "primary": "#037764",
        "secondary": "#d4561e",
        "accent": "#25d0b4",
        "warning": "#e8863a",
        "error": "#c94a16",
        "success": "#0fbda0",
    }
)

# Base2Tone Desert Theme
BASE2TONE_DESERT = Theme(
    name="base2tone-desert",
    primary="#816f4b",
    secondary="#d67e5c",
    warning="#eb9369",
    error="#d16846",
    success="#ac8e53",
    accent="#c6ad7b",
    dark=True,
    variables={
        "background": "#292724",
        "surface": "#3d3a34",
        "panel": "#615c51",
        "boost": "#908774",
        "dark": "#292724",
        "foreground": "#bbb4a5",
        "primary": "#816f4b",
        "secondary": "#d67e5c",
        "accent": "#c6ad7b",
        "warning": "#eb9369",
        "error": "#d16846",
        "success": "#ac8e53",
    }
)

# Base2Tone Drawbridge Theme
BASE2TONE_DRAWBRIDGE = Theme(
    name="base2tone-drawbridge",
    primary="#4961da",
    secondary="#ad5a3b",
    warning="#da7655",
    error="#b24a29",
    success="#7289fd",
    accent="#8b9efd",
    dark=True,
    variables={
        "background": "#1b1f32",
        "surface": "#252a41",
        "panel": "#444b6f",
        "boost": "#5e6587",
        "dark": "#1b1f32",
        "foreground": "#a6aab9",
        "primary": "#4961da",
        "secondary": "#ad5a3b",
        "accent": "#8b9efd",
        "warning": "#da7655",
        "error": "#b24a29",
        "success": "#7289fd",
    }
)

# Base2Tone Earth Theme
BASE2TONE_EARTH = Theme(
    name="base2tone-earth",
    primary="#6f5849",
    secondary="#ba663a",
    warning="#da7655",
    error="#b24a29",
    success="#88786d",
    accent="#a48774",
    dark=True,
    variables={
        "background": "#322d29",
        "surface": "#3f3a37",
        "panel": "#5b534d",
        "boost": "#796b63",
        "dark": "#322d29",
        "foreground": "#c7beb8",
        "primary": "#6f5849",
        "secondary": "#ba663a",
        "accent": "#a48774",
        "warning": "#da7655",
        "error": "#b24a29",
        "success": "#88786d",
    }
)

# Base2Tone Lake Theme
BASE2TONE_LAKE = Theme(
    name="base2tone-lake",
    primary="#2f7289",
    secondary="#c49144",
    warning="#e0ad69",
    error="#c9832f",
    success="#3e91ac",
    accent="#62b1cb",
    dark=True,
    variables={
        "background": "#192d34",
        "surface": "#223c44",
        "panel": "#335966",
        "boost": "#467686",
        "dark": "#192d34",
        "foreground": "#adc8d1",
        "primary": "#2f7289",
        "secondary": "#c49144",
        "accent": "#62b1cb",
        "warning": "#e0ad69",
        "error": "#c9832f",
        "success": "#3e91ac",
    }
)

# Base2Tone Meadow Theme
BASE2TONE_MEADOW = Theme(
    name="base2tone-meadow",
    primary="#1b6498",
    secondary="#b69027",
    warning="#d6ac49",
    error="#b58b1e",
    success="#277fbe",
    accent="#4299d7",
    dark=True,
    variables={
        "background": "#192834",
        "surface": "#223644",
        "panel": "#335166",
        "boost": "#466b86",
        "dark": "#192834",
        "foreground": "#7b9eb7",
        "primary": "#1b6498",
        "secondary": "#b69027",
        "accent": "#4299d7",
        "warning": "#d6ac49",
        "error": "#b58b1e",
        "success": "#277fbe",
    }
)

class SimpleRecorderApp(App):
    """A simple terminal GUI for screen recording."""
    
    ENABLE_COMMAND_PALETTE = True
    
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'recit'
        self.config_file = self.config_dir / 'config.json'
        
        # Load theme before super().__init__()
        saved_theme = None
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    saved_theme = config.get('theme')
        except:
            pass
        
        super().__init__()
        
        # Register custom themes FIRST
        self.register_theme(BASE2TONE_EVENING)
        self.register_theme(BASE2TONE_SEA)
        self.register_theme(BASE2TONE_FOREST)
        self.register_theme(BASE2TONE_FIELD)
        self.register_theme(BASE2TONE_DESERT)
        self.register_theme(BASE2TONE_DRAWBRIDGE)
        self.register_theme(BASE2TONE_EARTH)
        self.register_theme(BASE2TONE_LAKE)
        self.register_theme(BASE2TONE_MEADOW)
        
        # Apply saved theme after registration
        if saved_theme:
            self.theme = saved_theme
        
        self.recording_process = None
        self.recording_start_time = None
        
        # Load main config
        self.load_main_config()
        
        self.monitor_info = self.detect_monitor()
    
    def load_main_config(self):
        """Load recording settings from config.json."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.output_dir = config.get('output_dir', str(Path.home() / 'Videos' / 'Recordings'))
                    self.format = config.get('format', 'webm')
                    self.framerate = config.get('framerate', 30)
                    self.resolution = config.get('resolution', '720p')
            else:
                self.output_dir = str(Path.home() / 'Videos' / 'Recordings')
                self.format = 'webm'
                self.framerate = 30
                self.resolution = '720p'
        except:
            self.output_dir = str(Path.home() / 'Videos' / 'Recordings')
            self.format = 'webm'
            self.framerate = 30
            self.resolution = '720p'
        
        # Try to use the proper monitor detector
        try:
            import sys
            import os
            sys.path.insert(0, os.path.dirname(__file__))
            from monitor_utils import MonitorDetector
            detector = MonitorDetector()
            if detector.monitors:
                monitor = detector.get_primary_monitor()
                if monitor:
                    self.monitor_info = {
                        'resolution': monitor.resolution,
                        'width': monitor.width,
                        'height': monitor.height,
                        'aspect': monitor.aspect_ratio_string
                    }
        except:
            pass  # Use fallback detection
    
    def save_theme(self):
        """Save current theme to config."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            config = {}
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            config['theme'] = self.theme
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except:
            pass
    
    def watch_theme(self, theme: str) -> None:
        """Called when theme changes."""
        self.save_theme()
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    .info-panel {
        height: 7;
        border: round $primary;
        margin: 1 2 0 2;
        padding: 1 2;
    }
    
    .info-column {
        width: 50%;
        height: 100%;
    }
    
    .section-title {
        text-style: bold;
        color: $accent;
    }
    
    .info-line {
        padding-left: 2;
    }
    
    .controls {
        height: auto;
        dock: bottom;
        padding: 0;
    }
    
    .button-row {
        height: auto;
        margin-bottom: 1;
        padding: 0 2;
    }
    
    Button {
        margin: 0 1;
        width: 1fr;
        height: 3;
        border: none;
    }
    
    .button-row {
        height: auto;
        margin-bottom: 1;
    }
    
    .status {
        height: 3;
        background: $boost;
        padding: 1 2;
        border: none;
        margin: 0 2 1 2;
        content-align: center middle;
    }
    
    #status {
        width: 100%;
        height: 100%;
        content-align: center middle;
        color: $text;
        text-style: bold;
    }
    
    Button {
        margin: 0;
        width: 1fr;
        height: 3;
        border: none;
    }
    
    .record-button {
        background: $success 40%;
        color: $text;
    }
    
    .record-button:hover {
        background: $success 60%;
    }
    
    .stop-button {
        background: $accent 40%;
        color: $text;
    }
    
    .stop-button:hover {
        background: $accent 60%;
    }
    
    .utility-button {
        background: $primary 30%;
        color: $text;
    }
    
    .utility-button:hover {
        background: $primary 50%;
    }
    
    .exit-button {
        background: $panel 70%;
        color: $text;
    }
    
    .exit-button:hover {
        background: $boost 90%;
    }
    """
    
    BINDINGS = [
        ("r", "record_full", "Record"),
        ("a", "record_area", "Area"),
        ("s", "stop", "Stop"),
        ("m", "detect_monitor", "Monitor"),
        ("q", "quit", "Quit"),
        ("c", "command_palette", "Config"),
    ]
    
    recording = reactive(False)
    
    def detect_monitor(self):
        """Detect monitor information."""
        try:
            result = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if ' connected' in line and ('primary' in line or '*' in line):
                        # Extract resolution
                        import re
                        match = re.search(r'(\d+)x(\d+)', line)
                        if match:
                            width, height = int(match.group(1)), int(match.group(2))
                            aspect = width / height
                            if abs(aspect - 16/9) < 0.1:
                                aspect_str = "16:9"
                            elif abs(aspect - 21/9) < 0.1:
                                aspect_str = "21:9" 
                            elif abs(aspect - 32/9) < 0.1:
                                aspect_str = "32:9"
                            else:
                                aspect_str = f"{aspect:.2f}:1"
                            
                            return {
                                'resolution': f"{width}x{height}",
                                'width': width,
                                'height': height,
                                'aspect': aspect_str
                            }
        except:
            pass
        
        # Fallback
        return {
            'resolution': '1920x1080',
            'width': 1920,
            'height': 1080,
            'aspect': '16:9'
        }
    
    def compose(self) -> ComposeResult:
        """Create the layout."""
        with Container():
            with Horizontal(classes="info-panel"):
                with Vertical(classes="info-column"):
                    yield Static("Display", classes="section-title")
                    yield Static(f"{self.monitor_info['resolution']} • {self.monitor_info['aspect']}", id="resolution", classes="info-line")
                    yield Static("", id="output-info", classes="info-line")
                
                with Vertical(classes="info-column"):
                    yield Static("Settings", classes="section-title")
                    yield Static(f"{self.format.upper()} • {self.resolution} • {self.framerate} FPS", id="settings", classes="info-line")
                    yield Static("", id="file-info", classes="info-line")
            
            with Container(classes="status"):
                yield Static("Ready to record", id="status")
            
            with Vertical(classes="controls"):
                with Horizontal(classes="button-row"):
                    yield Button("🎬 Full Screen", id="record-full", classes="record-button")
                    yield Button("🎯 Select Area", id="record-area", classes="record-button") 
                    yield Button("⏹️  Stop", id="stop", classes="stop-button", disabled=True)
                
                with Horizontal(classes="button-row"):
                    yield Button("📁 Open Folder", id="open-folder", classes="utility-button")
                    yield Button("📸 PNG Area", id="png-area", classes="utility-button")
                    yield Button("📸 WebP Area", id="webp-area", classes="utility-button")
                    yield Button("❌ Exit", id="exit", classes="exit-button")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when app starts."""
        self.update_output_info()
    
    def update_output_info(self):
        """Update the output information display."""
        target_height = 720
        aspect_ratio = self.monitor_info['width'] / self.monitor_info['height']
        output_width = int(target_height * aspect_ratio)
        
        if output_width % 2 != 0:
            output_width += 1
        
        self.query_one("#output-info").update(
            f"Output: {output_width}x{target_height}"
        )
        
        bitrate_mbps = 1.0
        size_per_min_mb = bitrate_mbps * 60 / 8
        self.query_one("#file-info").update(
            f"~{size_per_min_mb:.1f} MB/min"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        if event.button.id == "record-full":
            self.start_recording(area_select=False)
        elif event.button.id == "record-area":
            self.start_recording(area_select=True)
        elif event.button.id == "stop":
            self.stop_recording()
        elif event.button.id == "open-folder":
            self.open_folder()
        elif event.button.id == "png-area":
            self.save_screenshot_file(area_select=True, format='png')
        elif event.button.id == "webp-area":
            self.save_screenshot_file(area_select=True, format='webp')
        elif event.button.id == "exit":
            self.exit()
    
    def start_recording(self, area_select=False):
        """Start recording."""
        if self.recording:
            return
        
        # Create output directory
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = Path(self.output_dir) / f'recording_{timestamp}.webm'
        
        # Build command
        cmd = ['ffmpeg', '-y']
        
        if area_select:
            self.query_one("#status").update("Select area with mouse, then return to this window...")
            self.refresh()
            
            try:
                # Use slop for area selection
                result = subprocess.run(['slop', '-f', '%x,%y,%w,%h'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    coords = result.stdout.strip().split(',')
                    if len(coords) == 4:
                        x, y, w, h = map(int, coords)
                        cmd.extend([
                            '-f', 'x11grab',
                            '-s', f'{w}x{h}',
                            '-i', f':0.0+{x},{y}',
                            '-r', '30'
                        ])
                    else:
                        self.query_one("#status").update("Area selection failed")
                        return
                else:
                    self.query_one("#status").update("Area selection cancelled")
                    return
            except:
                self.query_one("#status").update("Area selection failed (is slop installed?)")
                return
        else:
            # Full screen
            cmd.extend([
                '-f', 'x11grab',
                '-i', ':0.0',
                '-r', '30'
            ])
        
        # Add scaling for 720p with aspect ratio preservation (full screen only)
        if not area_select:
            cmd.extend(['-vf', 'scale=-1:720'])
        
        # WebM encoding
        cmd.extend(['-c:v', 'libvpx-vp9', '-crf', '32', '-b:v', '0'])
        cmd.append(str(output_file))
        
        try:
            self.recording_process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid
            )
            
            self.recording = True
            self.recording_start_time = time.time()
            self.output_file = output_file
            
            # Update UI
            self.query_one("#record-full").disabled = True
            self.query_one("#record-area").disabled = True
            self.query_one("#stop").disabled = False
            self.query_one("#status").update("🔴 Recording in progress...")
            
            # Start timer for progress updates
            self.set_timer(1.0, self.update_recording_status)
            
        except Exception as e:
            self.query_one("#status").update(f"❌ Failed to start recording: {e}")
    
    def stop_recording(self):
        """Stop recording."""
        if not self.recording or not self.recording_process:
            return
        
        try:
            # Send SIGTERM to stop recording
            os.killpg(os.getpgid(self.recording_process.pid), signal.SIGTERM)
            self.recording_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if needed
            os.killpg(os.getpgid(self.recording_process.pid), signal.SIGKILL)
        except Exception as e:
            self.query_one("#status").update(f"❌ Error stopping: {e}")
        
        self.recording = False
        self.recording_process = None
        
        # Update UI
        self.query_one("#record-full").disabled = False
        self.query_one("#record-area").disabled = False
        self.query_one("#stop").disabled = True
        
        # Show result
        if hasattr(self, 'output_file') and self.output_file.exists():
            size_mb = self.output_file.stat().st_size / (1024 * 1024)
            self.query_one("#status").update(
                f"✅ Recording saved: {self.output_file.name} ({size_mb:.1f} MB)"
            )
        else:
            self.query_one("#status").update("✅ Recording stopped")
    
    def update_recording_status(self):
        """Update recording status."""
        if not self.recording or not self.recording_start_time:
            return
        
        elapsed = time.time() - self.recording_start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        
        self.query_one("#status").update(f"🔴 Recording: {minutes:02d}:{seconds:02d}")
        
        if self.recording:
            self.set_timer(1.0, self.update_recording_status)
    
    def open_folder(self):
        """Open output folder."""
        try:
            subprocess.run(['xdg-open', self.output_dir])
        except:
            self.query_one("#status").update(f"Output folder: {self.output_dir}")
    
    def action_record_full(self):
        """Record full screen (R key)."""
        if not self.recording:
            self.start_recording(area_select=False)
    
    def action_record_area(self):
        """Record area (A key).""" 
        if not self.recording:
            self.start_recording(area_select=True)
    
    def action_stop(self):
        """Stop recording (S key)."""
        if self.recording:
            self.stop_recording()
    
    def action_detect_monitor(self):
        """Show monitor info (M key)."""
        self.show_monitor_detection()
    
    def show_monitor_detection(self):
        """Show detailed monitor detection info."""
        try:
            result = subprocess.run(['xrandr', '--query'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = []
                for line in result.stdout.split('\n'):
                    if ' connected' in line:
                        lines.append(line.strip())
                
                if lines:
                    info_text = "Detected monitors:\\n" + "\\n".join(lines[:3])
                else:
                    info_text = "No monitors detected via xrandr"
            else:
                info_text = "xrandr command failed"
        except:
            info_text = "Error running monitor detection"
        
        self.query_one("#status").update(info_text)
        self.set_timer(5.0, lambda: self.query_one("#status").update("Ready to record"))
    
    def save_screenshot_file(self, area_select=False, format='png'):
        """Save a screenshot using scrot and optionally convert to webp."""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_png = Path(self.output_dir) / f'screenshot_{timestamp}.png'
        final_file = Path(self.output_dir) / f'screenshot_{timestamp}.{format}'
        
        try:
            if area_select:
                self.query_one("#status").update("Select area with mouse...")
                self.refresh()
                
                result = subprocess.run(['slop', '-f', '%x,%y,%w,%h'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    coords = result.stdout.strip().split(',')
                    if len(coords) == 4:
                        x, y, w, h = coords
                        subprocess.run(['scrot', '-a', f'{x},{y},{w},{h}', str(temp_png)])
                        
                        if format == 'webp':
                            subprocess.run(['convert', str(temp_png), str(final_file)])
                            temp_png.unlink()
                            self.query_one("#status").update(f"✅ Screenshot saved: {final_file.name}")
                        else:
                            self.query_one("#status").update(f"✅ Screenshot saved: {temp_png.name}")
                    else:
                        self.query_one("#status").update("Area selection failed")
                else:
                    self.query_one("#status").update("Area selection cancelled")
            
            self.set_timer(3.0, lambda: self.query_one("#status").update("Ready to record"))
        except FileNotFoundError as e:
            if 'convert' in str(e):
                self.query_one("#status").update("❌ imagemagick not installed (sudo apt install imagemagick)")
            else:
                self.query_one("#status").update("❌ scrot not installed (sudo apt install scrot)")
            self.set_timer(3.0, lambda: self.query_one("#status").update("Ready to record"))
        except Exception as e:
            self.query_one("#status").update(f"❌ Failed: {e}")
            self.set_timer(3.0, lambda: self.query_one("#status").update("Ready to record"))

def main():
    """Run the app."""
    app = SimpleRecorderApp()
    app.run()

if __name__ == "__main__":
    main()