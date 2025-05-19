from checks.disk_encryption import is_disk_encrypted
from checks.antivirus import check_antivirus_status
from checks.os_updates import os_version
from checks.sleep_settings import timeout_settings
from daemon import start_daemon
if __name__ == "__main__":
    # encrypted_status = is_disk_encrypted()
    # print(f'disc encryption status : {encrypted_status}')

    # check_antivirus_status()
    # get_sleep_timeout_seconds()
    # timeout_settings()
    start_daemon()

