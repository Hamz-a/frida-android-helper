from frida_android_helper.utils import *


# Enabling and disabling is powered by https://stackoverflow.com/a/47476009
def enable_proxy(host=None, port="8080"):
    if host is None:
        host = get_ip_address()
        if host == "127.0.0.1":
            print("⚠️  Can't determine ip address, provide an IP or connect your PC to the interwebz")
            return
    if not port.isdigit():  # Just in case...
        port = 8080

    print("⚡️ Enabling the Android proxy...")
    for device in get_devices():
        print("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        device.shell("settings put global http_proxy {}:{}".format(host, port))
        result = device.shell("settings get global http_proxy")
        print("🔥 settings put global http_proxy {}:{} => {}".format(host, port, result.strip()))


def disable_proxy():
    print("⚡️ Disabling the Android proxy...")
    for device in get_devices():
        print("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        result = device.shell("settings delete global http_proxy")
        print("🔥 settings delete global http_proxy -> {}".format(result.strip()))

        result = device.shell("settings delete global global_http_proxy_host")
        print("🔥 settings delete global global_http_proxy_host -> {}".format(result.strip()))

        result = device.shell("settings delete global global_http_proxy_port")
        print("🔥 settings delete global global_http_proxy_port -> {}".format(result.strip()))

        perform_cmd(device, "am broadcast -a android.intent.action.PROXY_CHANGE", root=True)  # needs to be run as root
        print("🔥 Sent PROXY_CHANGE broadcast...")


def get_proxy():
    print("⚡️ Retrieving the Android proxy...")
    for device in get_devices():
        print("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        result = device.shell("settings get global http_proxy")
        print("🔥 settings get global http_proxy => {}".format(result.strip()))
