from frida_android_helper.utils import *


def enable_rproxy(port="8844"):
    eprint("⚡️ Enabling Android proxy via reverse tethering...")
    for device in get_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        eprint("🔥 Writing firewall rules...")
        perform_cmd(device, """"(iptables -t nat -F &&
        iptables -t nat -A OUTPUT -p tcp --dport 80 -j DNAT --to-destination 127.0.0.1:{port} &&
        iptables -t nat -A OUTPUT -p tcp --dport 443 -j DNAT --to-destination 127.0.0.1:{port} &&
        iptables -t nat -A POSTROUTING -p tcp --dport 80 -j MASQUERADE &&
        iptables -t nat -A POSTROUTING -p tcp --dport 443 -j MASQUERADE)"
        """.format(port=port), root=True)

        tcp_port = "tcp:{port}".format(port=port)
        eprint("🔥 Performing adb reverse {tcp_port} {tcp_port}...".format(tcp_port=tcp_port))
        reverse(device, tcp_port, tcp_port)


def disable_rproxy(port="8844"):
    eprint("⚡️ Disabling Android proxy via reverse tethering...")
    for device in get_devices():
        eprint("🔥 Cleaning firewall rules...")
        perform_cmd(device, "iptables -t nat -F", root=True)

        eprint("🔥 Performing adb reverse --remove tcp:{port}...".format(port=port))
        remove_reverse(device, "tcp:{port}".format(port=port))


def reverse(device, remote, local):
    # Temporary fix meanwhile this gets patched
    # https://github.com/Swind/pure-python-adb/pull/64
    cmd = "reverse:forward:{remote};{local}".format(remote=remote, local=local)
    conn = device.create_connection()
    with conn:
        conn.send(cmd)
        conn.check_status()


# Temporary fix meanwhile this gets accepted
# https://github.com/Swind/pure-python-adb/pull/65
def remove_reverse(device, remote):
    cmd = "reverse:killforward:{}".format(remote)
    conn = device.create_connection()
    with conn:
        conn.send(cmd)


def remove_reverse_all(device):
    for reverse in device.list_reverses():
        remove_reverse(reverse['remote'])
