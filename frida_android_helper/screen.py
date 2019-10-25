from datetime import datetime
from frida_android_helper.utils import *


def take_screenshot(filename=None):
    print("⚡ Taking a screenshot...")
    for device in get_devices():
        signature = get_device_model(device).replace(" ", "")
        if filename is None:
            filename = "{}_{}.png".format(signature, datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
        else:
            filename = "{}_{}.png".format(signature, filename)

        try:
            result = device.screencap()
            with open(filename, "wb") as f:
                f.write(result)
            print("🔥 Screeenshot saved {}".format(filename))
        except IndexError:
            print("⚠️ Activity probably protected by SECURE flag...")
            # todo implement frida hook to disable SECURE flag
