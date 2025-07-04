# Overwatch ME Server Blocker

Blocks Overwatch Middle East servers through Windows firewall rules.

![App Screenshot](https://i.imgur.com/gQqWQqY.png)

## What it does
- Blocks specific IP ranges used by Overwatch ME servers
- Simple GUI with block/unblock/delete buttons
- Works on Windows 10/11

## How to use
**Option 1: Download compiled version**
- Check the releases page for pre-built .exe files

**Option 2: Run from source**
1. Close Overwatch if it's running
2. Install Python requirements: `pip install -r requirements.txt`
3. Run: `python main.py`
4. Click Block to enable blocking (you can close the program after this and start playing)
5. Click Unblock when you want to disable blocking

Requires admin privileges to modify firewall rules.