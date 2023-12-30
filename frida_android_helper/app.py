from datetime import datetime
import os

from frida_android_helper.utils import *


def download_app(packagename=None):
    eprint("⚡️ Downloading app...")
    for device in get_adb_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        if packagename is None:  # get
            packagename = get_current_app_focus(device)
            if packagename is None:
                eprint("❌️ No app is open, specify package name.")
                continue
            packagenames = [packagename]
        else:
            packagenames = list_apps_for_device(device, packagename)
        if not packagenames:
            eprint("❌ No package with filter '{}' was found".format(packagename))

        for packagename in packagenames:
            eprint("🔥 Querying path info for {}...".format(packagename))
            path = perform_cmd(device, "pm path {}".format(packagename))
            packages = [p.replace('package:', '') for p in path.splitlines()]

            if not packages:
                eprint("❌ {} package does not exist.".format(packagename))
                continue

            folder = "{}_{}".format(packagename, datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
            eprint("🔥 Creating directory {}...".format(folder))
            os.mkdir(folder)

            for package in packages:
                save_package = "{}/{}".format(folder, os.path.basename(package))
                eprint("🔥 Downloading from {} to {}...".format(package, save_package))
                device.pull(package, save_package)


def list_apps(filter=None):
    if filter is None:
        filter = ""
        eprint("⚡️ List all packages...")
    else:
        eprint("⚡️ List packages using filter '{}'...".format(filter))

    for device in get_adb_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        for package in list_apps_for_device(device, filter):
            print(package)


def list_apps_for_device(device, filter=None):
    return [package for package in device.list_packages() if filter in package]

