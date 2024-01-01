from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from datetime import datetime, timedelta
from uuid import uuid4
from frida_android_helper.utils import *
import pkg_resources
import shutil
import appdirs
import os

PATH_CACHE_CA_DER = os.path.join(appdirs.user_data_dir("fah"), "fah_ca.der")

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

    eprint("⚡️ Caching fah_ca.der to {}...".format(PATH_CACHE_CA_DER))
    os.makedirs(os.path.dirname(PATH_CACHE_CA_DER), exist_ok=True)
    shutil.copyfile("fah_ca.der", PATH_CACHE_CA_DER)


def install_certificate(certificate=None):
    eprint("⚡️ Installing certificate...")
    # hardcoded one from running
    # openssl x509 -inform DER -subject_hash_old -in fah_ca.der
    x509_old_hash = "35aa2e12"
    if certificate is None:
        eprint("🔥 Certificate not specified, checking the existence of a default fah_ca.der...")
        if os.path.isfile("fah_ca.der"):
            eprint("🔥 Found fah_ca.der...")
            certificate = "fah_ca.der"
        elif os.path.isfile("cacert.der"):  # burp'ish
            eprint("🔥 Found cacert.der...")
            certificate = "cacert.der"
        elif os.path.isfile(PATH_CACHE_CA_DER):  # we got a cert in the cache!
            eprint("🔥 Found {}...".format(PATH_CACHE_CA_DER))
            certificate = PATH_CACHE_CA_DER
        else:
            eprint("❌ fah_ca.der / cacert.der not found...")
            return

        if os.path.isfile("fah_ca.der") or os.path.isfile("cacert.der"): # hacky: in case we didn't get it from cache...
            eprint("⚡️ Caching {} to {}...".format(certificate, PATH_CACHE_CA_DER))
            os.makedirs(os.path.dirname(PATH_CACHE_CA_DER), exist_ok=True)
            shutil.copyfile(certificate, PATH_CACHE_CA_DER)
    else:
        if os.path.isfile(certificate):
            eprint("🔥 Found {}...".format(certificate))
            # TODO: implement this using pure python cryptography module; it does not seem to be implemented (yet?)
            # So either leave this as it is, or re-implement the old hash ourselves...
            # https://github.com/openssl/openssl/blob/47b4ccea9cb9b924d058fd5a8583f073b7a41656/crypto/x509/x509_cmp.c#L207
            result = subprocess.run(
                ["openssl", "x509", "-inform", "DER", "-subject_hash_old", "-in", certificate, "-noout"],
                capture_output=True)
            if result.returncode == 0:
                x509_old_hash = result.stdout.strip().decode("utf-8")
                eprint("⚡️ Caching {} to {}...".format(certificate, PATH_CACHE_CA_DER))
                os.makedirs(os.path.dirname(PATH_CACHE_CA_DER), exist_ok=True)
                shutil.copyfile(certificate, PATH_CACHE_CA_DER)
            else:
                eprint("❌ {}".format(result.stderr.decode("utf-8")))
                return
        else:
            eprint("❌ {} not found...".format(certificate))
            return

    # install them certificates on devices
    for device in get_adb_devices():
        eprint("📲 Device: {} ({})".format(get_device_model(device), device.get_serial_no()))
        path_cacerts = "/system/etc/security/cacerts"
        offset = 0
        while "No such file or directory" not in \
                perform_cmd(device, "ls /system/etc/security/cacerts/{}.{}".format(x509_old_hash, offset)):
            eprint("❌ Found /system/etc/security/cacerts/{}.{}, incrementing by 1...".format(x509_old_hash, offset))
            offset += 1

        eprint("🔥 Pushing {} to {}/{}...".format(certificate, "/data/local/tmp", x509_old_hash))
        device.push(certificate, "/data/local/tmp/{}".format(x509_old_hash))

        # Powered by https://www.g1a55er.net/Android-14-Still-Allows-Modification-of-System-Certificates
        if get_android_version(device) >= 14:
            eprint("🔥 Detected Android 14+, we need a small detour...")
            eprint("    for more info, see: https://www.g1a55er.net/Android-14-Still-Allows-Modification-of-System-Certificates")
            path_cacerts = "/apex/com.android.conscrypt/cacerts"

            script = pkg_resources.resource_filename("frida_android_helper", "scripts/android14_apex.sh")
            eprint("🔥 Pushing android14_apex.sh script to /data/local/tmp/android14_apex.sh...")
            device.push(script, "/data/local/tmp/android14_apex.sh")

            eprint("🔥 chmod +x /data/local/tmp/android14_apex.sh...")
            err = perform_cmd(device, "chmod +x /data/local/tmp/android14_apex.sh", root=True)
            if err:
                eprint("❌ {}".format(err))
                continue
            eprint("🔥 Running /data/local/tmp/android14_apex.sh...")
            err = perform_cmd(device, "/data/local/tmp/android14_apex.sh", root=True)
            if err and "Device or resource busy" not in err:  # known error to ignore for now...
                eprint("❌ {}".format(err))
                continue
        else:
            eprint("🔥 Remounting the system rw: mount -o rw,remount /system...")
            err = perform_cmd(device, "mount -o rw,remount /system", root=True)
            if err:
                eprint("❌ {}".format(err))
                continue

        eprint("🔥 Moving the certificate to {}/{}.{}...".format(path_cacerts, x509_old_hash, offset))
        err = perform_cmd(device, "mv /data/local/tmp/{} {}/{}.{}".format(x509_old_hash, path_cacerts, x509_old_hash, offset), root=True)
        if err:
            eprint("❌ {}".format(err))
            continue

        eprint("🔥 Setting permissions root:root / 644")
        err = perform_cmd(device, "chown root:root {}/{}.{}".format(path_cacerts, x509_old_hash, offset), root=True)
        if err:
            eprint("❌ {}".format(err))
            continue
        err = perform_cmd(device, "chmod 644 {}/{}.{}".format(path_cacerts, x509_old_hash, offset), root=True)
        if err:
            eprint("❌ {}".format(err))
            continue

        if get_android_version(device) >= 14:
            perform_cmd(device, "killall system_server", root=True)
            eprint("✅ Soft rebooting now... Do not reboot your phone or you have to install the certificate again.")
        else:
            eprint("✅ Reboot your phone.")

