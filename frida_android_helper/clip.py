from frida_android_helper.utils import *
from frida_android_helper import frida_utils


def copy_from_clipboard():
    eprint("⚡️ Copy from clipboard...")
    for device in get_adb_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        app = get_current_app_focus(device)
        try:
            frida_utils.copy_from_clipboard(device, app)
        except Exception as err:
            eprint("❌ {}".format(err))
            eprint("❌ Is Frida running?")


def paste_to_clipboard(data):
    eprint("⚡️ Pasting '{}' to clipboard...".format(data))
    for device in get_adb_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        app = get_current_app_focus(device)
        try:
            frida_utils.paste_to_clipboard(device, app, data)
        except Exception as err:
            eprint("❌ {}".format(err))
            eprint("❌ Is Frida running?")

