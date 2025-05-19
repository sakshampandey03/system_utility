import platform
import subprocess

def is_disk_encrypted():
    system = platform.system()

    if system == "Windows":
        # Runs the command: manage-bde -status (checks BitLocker status)
        try:
            output = subprocess.check_output(["manage-bde", "-status"], stderr=subprocess.DEVNULL)
            return "Percentage Encrypted: 100%" in output.decode()
        except Exception:
            return False

    elif system == "Darwin":  # macOS
        # fdesetup is macOS's built-in tool for FileVault encryption
        try:
            output = subprocess.check_output(["fdesetup", "status"])
            return "FileVault is On." in output.decode()
        except Exception:
            return False

    elif system == "Linux":
        # Check for encrypted devices using lsblk (lists block devices)
        try:
            output = subprocess.check_output(["lsblk", "-o", "NAME,TYPE,MOUNTPOINT"])
            return b"crypt" in output
        except Exception:
            return False

    return False
