import subprocess
import re

def get_screen_timeout():
    """Get current screen timeout settings in seconds from powercfg output"""
    try:
        # Run powercfg command
        result = subprocess.run(["powercfg", "/query"], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode != 0:
            return f"Error running powercfg: {result.stderr}"
        
        # Parse the output
        output = result.stdout
        
        # Find the VIDEOIDLE section
        video_idle_match = re.search(
            r"Power Setting GUID:.*\(Turn off display after\)(.*?)Power Setting GUID", 
            output, 
            re.DOTALL
        )
        
        if not video_idle_match:
            return "Could not find screen timeout settings in powercfg output"
        
        video_idle_section = video_idle_match.group(1)
        
        # Extract AC and DC timeout values (hex to decimal)
        ac_match = re.search(r"Current AC Power Setting Index: 0x([0-9a-f]+)", video_idle_section)
        dc_match = re.search(r"Current DC Power Setting Index: 0x([0-9a-f]+)", video_idle_section)
        
        if not ac_match or not dc_match:
            return "Could not parse timeout values"
        
        ac_seconds = int(ac_match.group(1), 16)
        dc_seconds = int(dc_match.group(1), 16)
        
        return {
            "AC Timeout (seconds)": ac_seconds,
            "DC Timeout (seconds)": dc_seconds,
            "AC Timeout (minutes)": round(ac_seconds / 60, 1),
            "DC Timeout (minutes)": round(dc_seconds / 60, 1)
        }
        
    except Exception as e:
        return f"Error: {str(e)}"

def timeout_settings():
    timeout_settings = get_screen_timeout()
    print("Screen Timeout Settings:")
    print(f"On AC Power: {timeout_settings['AC Timeout (seconds)']} seconds ({timeout_settings['AC Timeout (minutes)']} minutes)")
    print(f"On Battery: {timeout_settings['DC Timeout (seconds)']} seconds ({timeout_settings['DC Timeout (minutes)']} minutes)")
    return timeout_settings['AC Timeout (seconds)']