
import platform
import subprocess

def check_antivirus_status():
    system = platform.system()

    if system == "Windows":
        try:
            import windows_tools.antivirus


            av_list = windows_tools.antivirus.get_installed_antivirus_software()
            for av in av_list:
                print(f"Name: {av['name']}")
                print(f"  Status: {'Enabled' if av['enabled'] else 'Disabled'}")
                print(f"  Up to date: {'Yes' if av['is_up_to_date'] else 'No'}\n")

            return av_list

        except Exception as e:
            print("Error retrieving antivirus information:", e)
            return []

    elif system == "Darwin":  # macOS
        known_av = ["Avast", "McAfee", "Norton", "Sophos", "Malwarebytes"]
        found = []
        for av in known_av:
            try:
                # Use Spotlight search to find the app
                result = subprocess.run(
                    ["mdfind", f"kMDItemDisplayName == '{av}'"],
                    capture_output=True, text=True
                )
                if result.stdout.strip():
                    found.append({"name": av, "enabled": True, "up_to_date": "Unknown"})
            except Exception as e:
                print(f"Error searching for {av}: {e}")
        return found if found else [{"name": "None", "enabled": False, "up_to_date": False}]

    elif system == "Linux":
        try:
            # Check if clamscan exists
            result = subprocess.run(
                ["which", "clamscan"], capture_output=True, text=True
            )
            if result.stdout.strip():
                # Check if clamd is running
                ps = subprocess.run(["ps", "aux"], capture_output=True, text=True)
                is_running = "clamd" in ps.stdout
                return [{
                    "name": "ClamAV",
                    "enabled": is_running,
                    "up_to_date": "Unknown"
                }]
            else:
                return [{"name": "None", "enabled": False, "up_to_date": False}]
        except Exception as e:
            print("Error checking antivirus on Linux:", e)
            return [{"name": "Unknown", "enabled": False, "up_to_date": False}]

    return [{"name": "Unknown", "enabled": False, "up_to_date": False}]

