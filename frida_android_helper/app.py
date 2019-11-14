from frida_android_helper.utils import *


def download_app(arg=None):
    print("download me")
    print(arg)


def list_apps(filter=None):
    if filter is None:
        filter = ""
        print("⚡️ List all packages...")
    else:
        print("⚡️ List packages using filter '{}'...".format(filter))

    for device in get_devices():
        print("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        for package in device.list_packages():
            if filter in package:
                print("📦  {}".format(package))
