import requests
import lzma
from frida_android_helper.utils import *


FRIDA_INSTALL_DIR = "/data/local/tmp/"
FRIDA_BIN_NAME = "frida-server"
FRIDA_LATEST_RELEASE_URL = "https://api.github.com/repos/frida/frida/releases/latest"


def download_latest_frida(device: Device):
    latest_release = requests.get(FRIDA_LATEST_RELEASE_URL).json()
    arch = get_architecture(device)

    for asset in latest_release['assets']:
        release_name = asset['name']
        if "server" in release_name and "android-{}.xz".format(arch) in release_name:
            print("⚡ Downloading {}...".format(release_name))
            xz_file = requests.get(asset['browser_download_url'])

            print("⚡ Extracting {}...".format(release_name))
            server_binary = lzma.decompress(xz_file.content)

            print("⚡ Writing {}...".format(release_name))
            with open(release_name[:-3], "wb") as f:  # remove extension
                f.write(server_binary)
            return release_name[:-3]


def launch_frida_server(device: Device):
    # hack: launch server, "forever sleep" and put in background. Short timeout to break off connection
    perform_cmd(device, "{}{} && sleep 2147483647 &".format(FRIDA_INSTALL_DIR, FRIDA_BIN_NAME), root=True, timeout=1)


def start_server():
    print("⚡ Starting frida-server")
    devices = get_devices()
    for device in devices:
        print("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        launch_frida_server(device)


def stop_server():
    print("⚡ Stopping frida-server")
    devices = get_devices()
    for device in devices:
        print("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        perform_cmd(device, "pkill frida-server", True)


def reboot_server():
    print("⚡ Rebooting frida-server")
    stop_server()
    start_server()


def update_server():
    print("⚡ Updating frida-server")
    devices = get_devices()
    for device in devices:
        print("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        server_binary = download_latest_frida(device)
        device.push(server_binary, "{}{}".format(FRIDA_INSTALL_DIR, FRIDA_BIN_NAME), 755)
        launch_frida_server(device)