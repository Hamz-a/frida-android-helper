import argparse
from frida_android_helper.screen import *
from frida_android_helper.server import *
from frida_android_helper.proxy import *
from frida_android_helper.snap import *
from frida_android_helper.cert import *


def main():
    arg_parser = argparse.ArgumentParser(prog="fah", description="Frida Android Helper")
    subparsers = arg_parser.add_subparsers(dest="func")

    server_group = subparsers.add_parser("server", help="Manage Frida server")
    server_group.add_argument("action", type=str, help="Frida server on Android", nargs="?",
                              choices=("start", "stop", "reboot", "update"))

    proxy_group = subparsers.add_parser("proxy", help="Configure Android proxy")
    proxy_group.add_argument("action", metavar="enable", type=str, help="Enable Android proxy", nargs="*", default=["set"])
    proxy_group.add_argument("disable", type=str, help="Delete Android proxy", nargs='?')
    proxy_group.add_argument("get", type=str, help="Get Android proxy settings", nargs='?')

    screen_group = subparsers.add_parser("screen", help="Take screenshot for evidence")
    screen_group.add_argument("action", metavar="filename", type=str, help="Specify filename", nargs="?", default=None)

    snap_group = subparsers.add_parser("snap", help="Make snapshots of data on disk")
    snap_group.add_argument("action", metavar="packagename", type=str, help="Specify packagename", nargs="?", default=None)

    cert_group = subparsers.add_parser("cert", help="Install CA for mitm purposes")
    cert_group.add_argument("action", metavar="cert", type=str, help="Specify certificate to install", nargs="?", default=None)


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
    elif args.func == "proxy":
        proxy_route = {
            "enable": enable_proxy,
            "disable": disable_proxy,
            "get": get_proxy
        }
        proxy_route.get(args.action[0], enable_proxy)(*args.action[1:2])
    elif args.func == "screen":
        take_screenshot(args.action)
    elif args.func == "snap":
        take_snapshot(args.action)
    elif args.func == "cert":
        install_cert(args.action)

    #print(args) # debugging purposes


if __name__ == '__main__':
    main()
