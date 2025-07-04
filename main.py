import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.admin import AdminManager
from src.core.app_controller import AppController
from src.gui.main_window import MainWindow
from src.utils.logger import Logger

class OverwatchFirewallManager:
    def __init__(self):
        # Check admin privileges
        if not AdminManager.is_admin():
            AdminManager.request_admin()
            return
        
        # Initialize components
        self.logger = Logger()
        
        # Initialize GUI with callbacks
        self.gui = MainWindow(
            on_block_callback=self.block_ips,
            on_unblock_callback=self.unblock_ips,
            on_delete_callback=self.delete_rules,
            on_scan_callback=self.scan_rules
        )
        
        # Initialize controller
        self.controller = AppController(self.gui, self.logger)
        
        # Initial scan
        self.controller.scan_rules()
    
    def block_ips(self):
        """Block IP addresses callback"""
        self.controller.block_ips()
    
    def unblock_ips(self):
        """Unblock IP addresses callback"""
        self.controller.unblock_ips()
    
    def delete_rules(self):
        """Delete rules callback"""
        self.controller.delete_rules()
    
    def scan_rules(self):
        """Scan rules callback"""
        self.controller.scan_rules()
    
    def run(self):
        """Start the application"""
        self.logger.log_success("Overwatch Firewall Manager started")
        self.gui.run()

if __name__ == "__main__":
    try:
        app = OverwatchFirewallManager()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        input("Press Enter to exit...")