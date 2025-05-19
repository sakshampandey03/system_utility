import platform
import subprocess
import os
import re

import subprocess

def run_cmd(script, timeout=120):
    result = subprocess.run(
        ["powershell", "-Command", script],
        capture_output=True,
        text=True,
        timeout=timeout
    )
    if(result.stderr):
        print("STDERR:\n", result.stderr)
    return result.stdout.strip()


def get_os_version():
    os_name = platform.system()

    if os_name == "Windows":
        return run_cmd("powershell -Command \"(Get-CimInstance Win32_OperatingSystem).Version\"")

    elif os_name == "Darwin":
        return run_cmd("sw_vers -productVersion")

    elif os_name == "Linux":
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("VERSION_ID"):
                        return line.split("=")[1].replace('"', '')
        return run_cmd("uname -r")

    return "Unsupported OS"

import win32com.client  # Requires pywin32 package

def get_available_os_version():
    os_name = platform.system()
    if os_name == "windows":
        try:
            update_session = win32com.client.Dispatch("Microsoft.Update.Session")
            searcher = update_session.CreateUpdateSearcher()
            
            try:
                search_result = searcher.Search("IsInstalled=0 and Type='Software'")
            except Exception as e:
                return f"Windows Update error: {str(e)}"
            
            updates = []
            for update in search_result.Updates:
                if "Windows" in update.Title:
                    updates.append({
                        'title': update.Title,
                        'kb': update.KBArticleIDs[0] if update.KBArticleIDs else None,
                        'version': re.search(r'\d+\.\d+\.\d+', update.Title)
                    })
            
            return updates if updates else "No Windows updates available"
        except Exception as e:
            return f"COM error: {str(e)}"

    elif os_name == "Darwin":
        updates = run_cmd("softwareupdate --list")
        matches = re.findall(r'\* Label: (.*?)\n', updates)
        return matches[0] if matches else "No updates available"

    elif os_name == "Linux":
        if os.path.exists("/usr/bin/apt"):
            run_cmd("sudo apt update > /dev/null")
            upgradable = run_cmd("apt list --upgradable")
            lines = [line for line in upgradable.splitlines() if "/" in line]
            available_versions = []
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    available_versions.append(f"{parts[0]} → {parts[1]}")
            return "\n".join(available_versions) if available_versions else "No updates available"
        elif os.path.exists("/usr/bin/dnf"):
            return run_cmd("dnf check-update") or "No updates available"
        else:
            return "Unsupported Linux distro"

    return "Unsupported OS"

def os_version():
    os_name = platform.system()
    print(f"🖥 OS Detected: {os_name}")
    print(f"🔎 Current OS Version: {get_os_version()}")
    print(f"🌐 Available Update Info:\n{get_available_os_version()}")