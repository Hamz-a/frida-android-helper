from frida_android_helper.utils import *
from frida_android_helper import frida_utils


def copy_from_clipboard():
    eprint("⚡️ Copy from clipboard...")
    for device in get_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        app, activity = get_current_app_focus(device)
        frida_utils.copy_from_clipboard(device, app)


def paste_to_clipboard(data):
    eprint("⚡️ Pasting '{}' to clipboard...".format(data))
    for device in get_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        app, activity = get_current_app_focus(device)
        frida_utils.paste_to_clipboard(device, app, data)

