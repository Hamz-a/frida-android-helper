import frida
import os
from adb.device import Device


def get_js_hook(js_filename):
    with open(os.path.join(os.path.dirname(__file__), "frida_hooks/{}".format(js_filename))) as f:
        return f.read()


def detached_callback(reason):
    print("🔰 Detached! Reason: {}".format(reason))


def message_callback(message, data):
    if message["type"] == "send":
        print("🔥 {}".format(message["payload"]))
    else:
        print("🐛 ".format(message))


# todo fix hook
# Error: android.view.ViewRootImpl$CalledFromWrongThreadException:
# Only the original thread that created a view hierarchy can touch its views.
def disable_secure_flag(device: Device, pkg_name, activity_name):
    js_code = "disable_secure_flag.js"
    device = frida.get_device(device.get_serial_no())
    session = device.attach(pkg_name)
    script = session.create_script(js_code)
    script.load()
    script.post({"activity": activity_name})  # Send data to JS agent
