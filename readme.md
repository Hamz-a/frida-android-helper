# Frida Android Helper

Currently the project only includes commands to start, stop, restart and most importantly update
the latest frida-server on your Android device.

It uses `pure-python-adb` to interface with the ADB server. The latest Android frida-server is fetched from GitHub
release page using the GitHub API. This is then installed on the Android device using `fah server update` command.


## Prerequisites
- Python 3
- ADB
- Rooted Android phone


## Installation
1. Clone the repository: `git clone https://github.com/Hamz-a/frida-android-helper`

2. Install `python3 setup.py install`


## Usage

Commands are self explanatory. Ask for help `fah --help`.

### Frida-server management

- Start the frida-server `fah server start`
- Stop the frida-server `fah server stop`
- Reboot the frida-server `fah server reboot`
- Update the frida-server `fah server update`

### Android proxy configuration

- Enable proxy:
    - `fah proxy`: will automatically select an IP address from your PC, default port 8080
    - `fah proxy enable`: same as above
    - `fah proxy enable 192.168.137.137`: specify IP address, default port 8080
    - `fah proxy enable 192.168.137.137 8888`: specify IP address and port
- Disable proxy `fah proxy disable`

 
## Ideas & bugs
Ideas and bug reports are welcome! 
