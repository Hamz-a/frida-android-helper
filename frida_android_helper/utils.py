from typing import List
import subprocess
import socket
import sys


import frida
from ppadb.client import Client as AdbClient
from ppadb.device import Device as AdbDevice


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_adb_devices() -> List[AdbDevice]:
    for attempt in range(2):
        try:
            client = AdbClient(host="127.0.0.1", port=5037)
            client.version()  # a random call to check if adb server is up
        except Exception as err:
            eprint(str(err))
            eprint("⚡ Starting ADB server...")
            subprocess.run(["adb", "start-server"])

    devices = client.devices()
    if len(devices) == 0:
        eprint("⚠️  no devices connected!")
    return devices


def perform_cmd(device: AdbDevice, command: str, root: bool = False, timeout: int = None):
    if root:
        command = "su -c {}".format(command)
    try:
        return device.shell(command, timeout=timeout)
    except:
        pass
        return ""


# https://stackoverflow.com/a/28950776
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("10.254.254.254", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def get_device_model(device: AdbDevice):
    return "{}_A{}".format(device.get_properties().get("ro.product.model", "Unknown").replace(" ", ""),
                    device.get_properties().get("ro.build.version.release", "Unknown"))


def get_architecture(device: AdbDevice):
    cpu = device.get_properties()["ro.product.cpu.abi"]
    if "arm64" in cpu:
        return "arm64"
    if "x86_64" in cpu:
        return "x86_64"
    if "arm" in cpu:
        return "arm"
    if "x86" in cpu:
        return "x86"
    return ""


def get_current_app_focus(device: AdbDevice):
    try:
        device = frida.get_device_matching(lambda d: d.id == device.get_serial_no())
        frontmost_app = device.get_frontmost_application()
        if frontmost_app:
            return frontmost_app.identifier
    except:
        pass
    return None


def get_current_activity(device: AdbDevice):
    # Sample: mCurrentFocus=Window{37b96ba u0 com.android.chrome/com.google.android.apps.chrome.Main}
    # When locked: mCurrentFocus=Window{5dd4bac u0 NotificationShade}
    result = perform_cmd(device, "dumpsys activity activities | grep mCurrentFocus")

    currentFocus = result.strip("\r\n{}").split(" ")[-1]
    if "/" in currentFocus:
        return currentFocus.split("/")[-1]
    else:
        eprint("⚠️  Device might be locked... (mCurrentFocus={})".format(currentFocus))
        return None

