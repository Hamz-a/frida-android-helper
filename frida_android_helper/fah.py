import argparse
import subprocess
import requests
import lzma
from adb.client import Client as AdbClient
from adb.device import Device


FRIDA_INSTALL_DIR = "/data/local/tmp/"
FRIDA_BIN_NAME = "frida-server"
FRIDA_LATEST_RELEASE_URL = "https://api.github.com/repos/frida/frida/releases/latest"


def get_architecture(device: Device):
    cpu = device.get_properties()['ro.product.cpu.abi']
    if "arm64" in cpu:
        return "arm64"
    if "x86_64" in cpu:
        return "x86_64"
    if "arm" in cpu:
        return "arm"
    if "x86" in cpu:
        return "x86"
    return ""


def download_latest_frida(device: Device):
    latest_release = requests.get(FRIDA_LATEST_RELEASE_URL).json()
    arch = get_architecture(device)

    for asset in latest_release['assets']:
        release_name = asset['name']
        if "server" in release_name and "android-{}.xz".format(arch) in release_name:
            print("Downloading {}...".format(release_name))
            xz_file = requests.get(asset['browser_download_url'])

            print("Extracting {}...".format(release_name))
            server_binary = lzma.decompress(xz_file.content)

            print("Writing {}...".format(release_name))
            with open(release_name[:-3], "wb") as f:  # remove extension
                f.write(server_binary)
            return release_name[:-3]


def launch_frida_server(device: Device):
    # hack: launch server, "forever sleep" and put in background. Short timeout to break off connection
    perform_cmd(device, "{}{} && sleep 2147483647 &".format(FRIDA_INSTALL_DIR, FRIDA_BIN_NAME), root=True, timeout=1)


def get_devices():
    for attempt in range(2):
        try:
            client = AdbClient(host="127.0.0.1", port=5037)
            client.version()  # a random call to check if adb server is up
        except Exception as err:
            print(str(err))
            print("Starting ADB server...")
            subprocess.run(["adb", "start-server"])

    devices = client.devices()
    if len(devices) == 0:
        print("⚠️  no devices connected!")
    return devices


def perform_cmd(device: Device, command: str, root: bool = False, timeout: int = None):
    if root:
        command = "su -c {}".format(command)
    try:
        return device.shell(command, timeout=timeout)
    except:
        pass


def start_server():
    print("Starting frida-server")
    devices = get_devices()
    for device in devices:
        launch_frida_server(device)


def stop_server():
    print("Stopping Frida server")
    devices = get_devices()
    for device in devices:
        perform_cmd(device, "pkill frida-server", True)


def reboot_server():
    print("Rebooting frida-server")
    stop_server()
    start_server()


def update_server():
    print("update")
    devices = get_devices()
    for device in devices:
        server_binary = download_latest_frida(device)
        device.push(server_binary, "{}{}".format(FRIDA_INSTALL_DIR, FRIDA_BIN_NAME), 755)
        launch_frida_server(device)


def main():
    arg_parser = argparse.ArgumentParser(prog="fah", description="Frida Android Helper")
    subparsers = arg_parser.add_subparsers(dest="func")

    server_group = subparsers.add_parser("server", help="Manage Frida server")
    server_group.add_argument("action", type=str, help="Frida server on Android", nargs="?",
                              choices=("start", "stop", "reboot", "update"))

    args = arg_parser.parse_args()

    if not args.func:
        arg_parser.print_help()

    if args.func == "server":
        server_route = {
            "start": start_server,
            "stop": stop_server,
            "reboot": reboot_server,
            "update": update_server
        }

        server_route.get(args.action, start_server)()


if __name__ == '__main__':
    main()
