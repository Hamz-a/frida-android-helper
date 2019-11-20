import subprocess
import socket
import sys

from ppadb.client import Client as AdbClient
from ppadb.device import Device


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_devices():
    for attempt in range(2):
        try:
            client = AdbClient(host="127.0.0.1", port=5037)
            client.version()  # a random call to check if adb server is up
        except Exception as err:
            print(str(err))
            print("⚡ Starting ADB server...")
            subprocess.run(["adb", "start-server"])

    devices = client.devices()
    if len(devices) == 0:
        print("⚠️  no devices connected!")
    return devices


def perform_cmd(device: Device, command: str, root: bool = False, timeout: int = None):
    if root:
        command = "su -c {}".format(command)
    try:
        return device.shell(command, timeout=timeout)
    except:
        pass
        return ""


def get_ip_address():  # might need refactoring...
    return socket.gethostbyname(socket.gethostname())


def get_device_model(device: Device):
    return "{} {}".format(device.get_properties().get("ro.vendor.product.manufacturer", "Unknown"),
                          device.get_properties().get("ro.vendor.product.model", "Unkown"))


def get_architecture(device: Device):
    cpu = device.get_properties()['ro.product.cpu.abi']
    if "arm64" in cpu:
        return "arm64"
    if "x86_64" in cpu:
        return "x86_64"
    if "arm" in cpu:
        return "arm"
    if "x86" in cpu:
        return "x86"
    return ""


def get_current_app_focus(device: Device):
    # Sample: mCurrentFocus=Window{127ced0 u0 com.android.launcher3/com.android.searchlauncher.SearchLauncher}
    # When locked: mCurrentFocus=Window{8f41b66 u0 StatusBar}
    result = perform_cmd(device, "dumpsys window windows | grep mCurrentFocus")

    currentFocus = result.strip("\r\n{}").split(" ")[-1]
    if "/" in currentFocus:
        return currentFocus.split("/")
    else:
        print("⚠️  Device might be locked... (mCurrentFocus={})".format(currentFocus))
        return [currentFocus, ""]
