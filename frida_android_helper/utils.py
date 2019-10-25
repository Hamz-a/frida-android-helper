import subprocess
import socket

from adb.client import Client as AdbClient
from adb.device import Device


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


def get_ip_address():  # might need refactoring...
    return socket.gethostbyname(socket.gethostname())


def get_device_model(device: Device):
    return "{} {}".format(device.get_properties()["ro.vendor.product.manufacturer"],
                          device.get_properties()["ro.vendor.product.model"])


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
