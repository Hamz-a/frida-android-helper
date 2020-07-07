import pkg_resources
import frida


def destroyed_callback(reason):
    print("🔰 Destroyed! Reason: {}".format(reason))


def message_callback(message, data):
    if message["type"] == "send":
        print("🔥 {}".format(message["payload"]))
    else:
        print("🐛 ".format(message))


def get_js_hook(js_filename):
    return pkg_resources.resource_string("frida_android_helper", "frida_hooks/{}".format(js_filename)).decode("utf-8")


def load_script_with_device(device, pkg_name, js_file):
    js_code = get_js_hook(js_file)
    device = frida.get_device(device.get_serial_no())
    session = device.attach(pkg_name)
    script = session.create_script(js_code)
    script.on("message", message_callback)
    script.load()
    return script


def disable_secure_flag(device, pkg_name, activity_name):
    print('📦 {}'.format(pkg_name))
    script = load_script_with_device(device, pkg_name, "disable_secure_flag.js")
    script.exports.disablesecureflag(activity_name)


def copy_from_clipboard(device, pkg_name):
    print('📦 {}'.format(pkg_name))
    script = load_script_with_device(device, pkg_name, "clipboard.js")
    script.exports.copyfromclipboard()


def paste_to_clipboard(device, pkg_name, data):
    print("data: '{}'".format(data))
    print('📦 {}'.format(pkg_name))
    script = load_script_with_device(device, pkg_name, "clipboard.js")
    script.exports.pastetoclipboard(data)
