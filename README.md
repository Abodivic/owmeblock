# Overwatch ME Server Blocker

Blocks Overwatch Middle East servers through Windows firewall rules.

![App Screenshot](https://i.imgur.com/gQqWQqY.png)

## What it does
- Blocks specific IP ranges used by Overwatch ME servers
- Simple GUI with block/unblock/delete buttons
- Works on Windows 10/11

## How to use
Run this tool before running Overwatch otherwise you'll remain on whatever servers you're already connected to

**Option 1: Download compiled version**
1. Download the release version
2. Run the tool, click on Block
3. Start Overwatch and enjoy non-Middle Eastern lobbies

**Option 2: Run from source**
1. Install Python requirements: `pip install -r requirements.txt`
2. Run: `python main.py`
3. Click Block to enable blocking (you can close the program after this and start playing)
4. Click Unblock when you want to disable blocking

Requires admin privileges to modify firewall rules.
