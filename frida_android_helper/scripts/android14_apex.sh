# Credits: https://www.g1a55er.net/Android-14-Still-Allows-Modification-of-System-Certificates
# Deal with the fact that there will be executables on the /apex tmpfs
# !! Not suitable for production usage !! 
setenforce 0
mount -o remount,exec /apex
# Make a copy of the current conscrypt APEX contents
cp -r -p /apex/com.android.conscrypt /apex/com.android.conscrypt-bak
sleep 1
# Lazily unmount because conscrypt might be in active use
umount -l /apex/com.android.conscrypt
sleep 1
rm -rf /apex/com.android.conscrypt
# Put contents of conscrypt APEX on /apex tmpfs mount
mv /apex/com.android.conscrypt-bak/* /apex/com.android.conscrypt/
# Soft userspace reboot to get everything back into a consistent state 
# killall system_server