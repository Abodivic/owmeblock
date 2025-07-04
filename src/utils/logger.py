from datetime import datetime
from typing import Optional

class Logger:
    def __init__(self, log_widget=None):
        self.log_widget = log_widget
        self.root = None
    
    def set_log_widget(self, widget, root):
        """Set the log widget and root window for GUI logging"""
        self.log_widget = widget
        self.root = root
    
    def log_message(self, message: str, level: str = "INFO"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        if self.log_widget and self.root:
            self.log_widget.insert("end", log_entry)
            self.log_widget.see("end")
            self.root.update_idletasks()
        else:
            print(log_entry.strip())
    
    def log_success(self, message: str):
        """Log success message"""
        self.log_message(message, "SUCCESS")
    
    def log_error(self, message: str):
        """Log error message"""
        self.log_message(message, "ERROR")
    
    def log_warning(self, message: str):
        """Log warning message"""
        self.log_message(message, "WARNING")
    
    def log_info(self, message: str):
        """Log info message"""
        self.log_message(message, "INFO")