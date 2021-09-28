from frida_android_helper.utils import *
import frida


def list_processes(search):
    eprint("⚡️ Listing processes...")
    for device in get_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        frida_device = frida.get_device(device.get_serial_no())
        for app in frida_device.enumerate_applications():
            if search.lower() in app.identifier.lower() or search.lower() in app.name.lower():
                print("🌕 {} ({}) [{}]".format(app.name, app.identifier, app.pid))
