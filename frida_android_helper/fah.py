import argparse

from frida_android_helper.screen import *
from frida_android_helper.server import *
from frida_android_helper.proxy import *
from frida_android_helper.rproxy import *
from frida_android_helper.snap import *
from frida_android_helper.cert import *
from frida_android_helper.app import *
from frida_android_helper.clip import *
from frida_android_helper.ps import *
from frida_android_helper.input import *

def main():
    arg_parser = argparse.ArgumentParser(prog="fah", description="Frida Android Helper")
    subparsers = arg_parser.add_subparsers(dest="func")

    server_group = subparsers.add_parser("server", help="Manage Frida server")
    server_group.add_argument("action", type=str, help="Frida server on Android", nargs="?",
                              choices=("start", "stop", "reboot", "update"))

    proxy_group = subparsers.add_parser("proxy", help="Configure Android proxy")
    proxy_group.add_argument("action", metavar="enable", type=str, help="Enable Android proxy", nargs="*", default=["set"])
    proxy_group.add_argument("disable", type=str, help="Disable Android proxy", nargs="?")
    proxy_group.add_argument("get", type=str, help="Get Android proxy settings", nargs="?")

    rproxy_group = subparsers.add_parser("rproxy", help="Configure Android proxy via reverse tethering")
    rproxy_group.add_argument("action", metavar="enable", type=str, help="Enable Android proxy via reverse tethering", nargs="*", default=["set"])
    rproxy_group.add_argument("disable", type=str, help="Disable Android proxy via reverse tethering", nargs="?")

    screen_group = subparsers.add_parser("screen", help="Take screenshot for evidence")
    screen_group.add_argument("action", metavar="filename", type=str, help="Specify filename", nargs="?", default=None)

    snap_group = subparsers.add_parser("snap", help="Make snapshots of data on disk")
    snap_group.add_argument("action", metavar="packagename", type=str, help="Specify packagename", nargs="?", default=None)

    cert_group = subparsers.add_parser("cert", help="Certificate creation & installation for mitm purposes")
    cert_group.add_argument("action", metavar="generate", type=str, help="Generate certificate", nargs="*", default=["generate"])
    cert_group.add_argument("install", type=str, help="Install a certificate", nargs="?")
    cert_group.add_argument("setup", type=str, help="Generate & install certificate", nargs="?")

    app_group = subparsers.add_parser("app", help="List and download apps from device")
    app_group.add_argument("action", metavar="dl", type=str, help="Download Android app", nargs="*", default=["dl"])
    app_group.add_argument("list", type=str, help="List installed Android apps", nargs="?")

    clip_group = subparsers.add_parser("clip", help="Manage Android's clipboard")
    clip_group.add_argument("action", metavar="copy", type=str, help="Copy from Android's clipboard", nargs="*", default=["copy"])
    clip_group.add_argument("paste", type=str, help="Paste to Android's clipboard", nargs="?")

    ps_group = subparsers.add_parser("ps", help="List Android's processes")
    ps_group.add_argument("action", metavar="ps", type=str, help="List Android's processes", nargs="*", default=None)

    input_group = subparsers.add_parser("input", help="Input manipulation")
    input_group.add_argument("action", metavar="text", type=str, help="Write to input", nargs="*", default=None)

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
        proxy_route.get(args.action[0], enable_proxy)(*args.action[1:3])
    elif args.func == "screen":
        take_screenshot(args.action)
    elif args.func == "snap":
        take_snapshot(args.action)
    elif args.func == "cert":
        cert_route = {
            "generate": generate_certificate,
            "install": install_certificate,
            "setup": setup_certificate,
        }
        cert_route.get(args.action[0], generate_certificate)(*args.action[1:2])
    elif args.func == "app":
        app_route = {
            "dl": download_app,
            "list": list_apps,
        }
        app_route.get(args.action[0], download_app)(*args.action[1:2])
    elif args.func == "clip":
        if args.action[0] == "copy":
            copy_from_clipboard()
        elif args.action[0] == "paste":
            paste_to_clipboard(" ".join(args.action[1:]))
        else:
            paste_to_clipboard(" ".join(args.action))
    elif args.func == "rproxy":
        rproxy_route = {
            "enable": enable_rproxy,
            "disable": disable_rproxy
        }
        rproxy_route.get(args.action[0], enable_rproxy)(*args.action[1:2])
    elif args.func == "ps":
        list_processes(" ".join(args.action))
    elif args.func == "input":
        if args.action[0] == "text":
            input_text(" ".join(args.action[1:]))
    #print(args) # debugging purposes


if __name__ == "__main__":
    main()
