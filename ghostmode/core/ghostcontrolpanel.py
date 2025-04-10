# Load and patch ghostcontrolpanel.py to:
# - Use sys._MEIPASS-safe paths
# - Fix subprocess calls to use sys.executable

ghostcontrol_path = os.path.join(extract_path, "ghostmode", "core", "ghostcontrolpanel.py")

with open(ghostcontrol_path, "r", encoding="utf-8") as f:
    original_code = f.read()

# Patch logic to use sys.executable and sys._MEIPASS if frozen
patch_header = '''
import sys
import subprocess
import os

def get_tool_path(rel_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.dirname(__file__), "..", rel_path)

def run_tool(script_rel_path):
    script_path = get_tool_path(script_rel_path)
    subprocess.run([sys.executable, script_path])
'''

# Replace old manual subprocess calls (basic structure) with our run_tool pattern
# For now, we'll just insert the helper functions at the top of the file
if "def get_tool_path" not in original_code:
    patched_code = patch_header + "\n" + original_code
else:
    patched_code = original_code  # already patched

# Save patched version
patched_path = "/mnt/data/ghostcontrolpanel_patched.py"
with open(patched_path, "w", encoding="utf-8") as f:
    f.write(patched_code)

patched_path
