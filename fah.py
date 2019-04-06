import argparse


def start_server():
    print("start")


def stop_server():
    print("stop")


def reboot_server():
    stop_server()
    start_server()


def update_server():
    print("update")


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
