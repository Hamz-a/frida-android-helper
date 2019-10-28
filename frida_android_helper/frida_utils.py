import frida
import os


def get_js_hook(js_filename):
    with open(os.path.join(os.path.dirname(__file__), "frida_hooks/{}".format(js_filename))) as f:
        return f.read()


def destroyed_callback(reason):
    print("🔰 Destroyed! Reason: {}".format(reason))


def message_callback(message, data):
    if message["type"] == "send":
        print("🔥 {}".format(message["payload"]))
    else:
        print("🐛 ".format(message))


def disable_secure_flag(device, pkg_name, activity_name):
    js_code = get_js_hook("disable_secure_flag.js")
    device = frida.get_device(device.get_serial_no())
    session = device.attach(pkg_name)
    script = session.create_script(js_code)
    script.on("message", message_callback)
    script.load()
    script.exports.disablesecureflag(activity_name)


