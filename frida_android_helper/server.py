import requests
import lzma
from frida_android_helper.utils import *
from ppadb.device import Device as AdbDevice

FRIDA_INSTALL_DIR = "/data/local/tmp/"
FRIDA_BIN_NAME = "frida-server"
FRIDA_LATEST_RELEASE_URL = "https://api.github.com/repos/frida/frida/releases/latest"


def download_latest_frida(device: AdbDevice):
    latest_release = requests.get(FRIDA_LATEST_RELEASE_URL).json()
    arch = get_architecture(device)

    for asset in latest_release['assets']:
        release_name = asset['name']
        if "server" in release_name and "android-{}.xz".format(arch) in release_name:
            eprint("⚡ Downloading {}...".format(release_name))
            xz_file = requests.get(asset['browser_download_url'])

            eprint("⚡ Extracting {}...".format(release_name))
            server_binary = lzma.decompress(xz_file.content)

            eprint("⚡ Writing {}...".format(release_name))
            with open(release_name[:-3], "wb") as f:  # remove extension
                f.write(server_binary)
            return release_name[:-3]


def launch_frida_server(device: AdbDevice):
    # hack: launch server, "forever sleep" and put in background. Short timeout to break off connection
    err = perform_cmd(device, "{}{} && sleep 2147483647 &".format(FRIDA_INSTALL_DIR, FRIDA_BIN_NAME), root=True, timeout=1)
    if err:
        eprint("❌ {}".format(err))



def start_server():
    eprint("⚡️ Starting frida-server")
    devices = get_adb_devices()
    for device in devices:
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        launch_frida_server(device)


def stop_server():
    eprint("⚡️ Stopping frida-server")
    devices = get_adb_devices()
    for device in devices:
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        err = perform_cmd(device, "pkill frida-server", root=True)
        if err:
            eprint("❌ {}".format(err))
            continue


def reboot_server():
    eprint("⚡️ Rebooting frida-server")
    stop_server()
    start_server()


def update_server():
    eprint("⚡️ Updating frida-server")
    devices = get_adb_devices()
    for device in devices:
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        server_binary = download_latest_frida(device)
        device.push(server_binary, "{}{}".format(FRIDA_INSTALL_DIR, FRIDA_BIN_NAME), 755)
        launch_frida_server(device)
