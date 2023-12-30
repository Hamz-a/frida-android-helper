from frida_android_helper.utils import *


def input_text(text):
    eprint("⚡️ Inserting text '{}'...".format(text))
    for device in get_adb_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        perform_cmd(device, "input text {}".format(text))
        print(device.get_frontmost_application())

