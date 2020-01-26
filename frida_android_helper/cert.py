from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from datetime import datetime, timedelta
from uuid import uuid4
from frida_android_helper.utils import *
from os.path import isfile


def setup_certificate(_=None):
    eprint("⚡️ Setting up your device certificate...")
    generate_certificate()
    install_certificate()


def generate_certificate(_=None):
    eprint("⚡️ Generating certificate...")

    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()
    builder = x509.CertificateBuilder().subject_name(x509.Name([
        x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, "DZ"),
        x509.NameAttribute(x509.oid.NameOID.STATE_OR_PROVINCE_NAME, "ORAN"),
        x509.NameAttribute(x509.oid.NameOID.LOCALITY_NAME, "ORAN"),
        x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, "FAH Corp"),
        x509.NameAttribute(x509.oid.NameOID.ORGANIZATIONAL_UNIT_NAME, "FAH"),
        x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "FAH CA"),
        x509.NameAttribute(x509.oid.NameOID.EMAIL_ADDRESS, "info@example.com"),
    ])).issuer_name(x509.Name([
        x509.NameAttribute(x509.oid.NameOID.COUNTRY_NAME, "DZ"),
        x509.NameAttribute(x509.oid.NameOID.STATE_OR_PROVINCE_NAME, "ORAN"),
        x509.NameAttribute(x509.oid.NameOID.LOCALITY_NAME, "ORAN"),
        x509.NameAttribute(x509.oid.NameOID.ORGANIZATION_NAME, "FAH Corp"),
        x509.NameAttribute(x509.oid.NameOID.ORGANIZATIONAL_UNIT_NAME, "FAH"),
        x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "FAH CA"),
        x509.NameAttribute(x509.oid.NameOID.EMAIL_ADDRESS, "info@example.com"),
    ])).not_valid_before(datetime.today() - timedelta(days=1))\
        .not_valid_after(datetime.today() + timedelta(days=365 * 2))\
        .serial_number(int(uuid4()))\
        .public_key(public_key)\
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)

    certificate = builder.sign(
        private_key=private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    eprint("⚡️ Writing fah_server_private_key.der...")
    with open("fah_server_private_key.der", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    eprint("⚡️ Writing fah_ca.der...")
    with open("fah_ca.der", "wb") as f:
        f.write(certificate.public_bytes(
            encoding=serialization.Encoding.DER
        ))


def install_certificate(certificate=None):
    eprint("⚡️ Installing certificate...")
    # hardcoded one from running
    # openssl x509 -inform DER -subject_hash_old -in fah_ca.der
    x509_old_hash = "35aa2e12"
    if certificate is None:
        eprint("🔥 Certificate not specified, checking the existence of a default fah_ca.der...")
        if isfile("fah_ca.der"):
            eprint("🔥 Found fah_ca.der...")
            certificate = "fah_ca.der"
        else:
            eprint("❌ fah_ca.der not found...")
            return
    else:
        if isfile(certificate):
            eprint("🔥 Found {}...".format(certificate))
            # TODO: implement this using pure python cryptography module; it does not seem to be implemented (yet?)
            # So either leave this as it is, or re-implement the old hash ourselves...
            # https://github.com/openssl/openssl/blob/47b4ccea9cb9b924d058fd5a8583f073b7a41656/crypto/x509/x509_cmp.c#L207
            result = subprocess.run(
                ["openssl", "x509", "-inform", "DER", "-subject_hash_old", "-in", certificate, "-noout"],
                capture_output=True)
            if result.returncode == 0:
                x509_old_hash = result.stdout.strip().decode("utf-8")
            else:
                eprint("❌ {}".format(result.stderr.decode("utf-8")))
                return
        else:
            eprint("❌ {} not found...".format(certificate))
            return

    # install them certificates on devices
    for device in get_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        eprint("🔥 Pushing {} to {}/{}...".format(certificate, "/data/local/tmp", x509_old_hash))
        device.push(certificate, "/data/local/tmp/{}".format(x509_old_hash))

        offset = 0
        while "No such file or directory" not in \
            perform_cmd(device, "ls /system/etc/security/cacerts/{}.{}".format(x509_old_hash, offset)):
            eprint("❌ Found /system/etc/security/cacerts/{}.{}, incrementing by 1...".format(x509_old_hash, offset))
            offset += 1

        eprint("🔥 Remounting the system rw: mount -o rw,remount /system...")
        perform_cmd(device, "mount -o rw,remount /system", root=True)
        eprint("🔥 Moving the certificate to /system/etc/security/cacerts/{}.{}...".format(x509_old_hash, offset))
        perform_cmd(device, "mv /data/local/tmp/{} /system/etc/security/cacerts/{}.{}"
                    .format(x509_old_hash, x509_old_hash, offset), root=True)
        eprint("🔥 Setting permissions root:root / 644")
        perform_cmd(device, "chown root:root /system/etc/security/cacerts/{}.{}".format(x509_old_hash, offset), root=True)
        perform_cmd(device, "chmod 644 /system/etc/security/cacerts/{}.{}".format(x509_old_hash, offset), root=True)
        eprint("✅ Reboot your phone.")
