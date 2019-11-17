from datetime import datetime
from frida_android_helper.utils import *


def download_app(packagename=None):
    print("⚡️ Downloading app...")
    for device in get_devices():
        print("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        if packagename is None:  # get
            packagename, _ = get_current_app_focus(device)
            if packagename == "StatusBar":
                print("❌️ Unlock device or specify package name.")
                continue

        print("🔥 Querying path info for {}...".format(packagename))
        path = perform_cmd(device, "pm path {}".format(packagename)).strip().replace("package:", "", 1)

        if not path:
            print("❌ {} package does not exist.".format(packagename))
            continue

        save_apk = "{}_{}.apk".format(packagename, datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
        print("🔥 Downloading from {} to {}...".format(path, save_apk))
        device.pull(path, save_apk)


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
