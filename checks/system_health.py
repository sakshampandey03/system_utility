
from .os_updates import get_os_version, get_available_os_version
from .antivirus import check_antivirus_status
from .sleep_settings import timeout_settings
from .disk_encryption import is_disk_encrypted

def get_system_health_snapshot():
    return {
        "os_version": get_os_version(),
        "available_update": get_available_os_version(),
        "antivirus": check_antivirus_status(),
        "sleep_timeout_seconds": timeout_settings(),
        "disk_encryption_status": is_disk_encrypted(),
    }
