import ctypes
import sys
import os

class AdminManager:
    @staticmethod
    def is_admin() -> bool:
        """Check if running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def request_admin():
        """Request administrator privileges"""
        if sys.argv[0].endswith('.py'):
            # Running as Python script
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{os.path.abspath(sys.argv[0])}"', None, 1
            )
        else:
            # Running as executable
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.argv[0], "", None, 1
            )
        sys.exit(0)