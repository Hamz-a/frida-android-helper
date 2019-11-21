from datetime import datetime

from frida_android_helper.utils import *


def download_app(packagename=None):
    eprint("⚡️ Downloading app...")
    for device in get_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        if packagename is None:  # get
            packagename, _ = get_current_app_focus(device)
            if packagename == "StatusBar":
                eprint("❌️ Unlock device or specify package name.")
                continue

        eprint("🔥 Querying path info for {}...".format(packagename))
        path = perform_cmd(device, "pm path {}".format(packagename)).strip().replace("package:", "", 1)

        if not path:
            eprint("❌ {} package does not exist.".format(packagename))
            continue

        save_apk = "{}_{}.apk".format(packagename, datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
        eprint("🔥 Downloading from {} to {}...".format(path, save_apk))
        device.pull(path, save_apk)


def list_apps(filter=None):
    if filter is None:
        filter = ""
        eprint("⚡️ List all packages...")
    else:
        eprint("⚡️ List packages using filter '{}'...".format(filter))

    for device in get_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        for package in device.list_packages():
            if filter in package:
                # Print this to stdout because someone might like to pipe the
                # list to another command
                print(package)
