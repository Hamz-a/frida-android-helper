from datetime import datetime
from frida_android_helper.utils import *


def take_snapshot(packagename=None):
    eprint("⚡️ Taking a snapshot...")
    for device in get_adb_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        if packagename is None:  # get
            packagename = get_current_app_focus(device)
            if packagename is None:
                eprint("❌️ No app is open, specify package name.")
                continue

        directory_name = "{}_{}".format(packagename, datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))

        eprint("🔥 Copying from /data/data/{} to /sdcard/Download/{}...".format(packagename, directory_name))
        err = perform_cmd(device, "cp -Lpr /data/data/{} /sdcard/Download/{}".format(packagename, directory_name), root=True)
        if err:
            eprint("❌ {}".format(err))
            continue

        eprint("🔥 Downloading from /sdcard/Download/{}...".format(directory_name))
        # https://github.com/Swind/pure-python-adb/issues/28
        # device.pull("/sdcard/Download/{}/".format(packagename), directory_name)
        subprocess.run(["adb", "pull", "/sdcard/Download/{}".format(directory_name)])

        eprint("🔥 Cleaning up /sdcard/Download/{}...".format(directory_name))
        perform_cmd(device, "rm -rf /sdcard/Download/{}".format(directory_name))
