# Frida Android Helper

Several handy commands to facilitate common Android pentesting tasks.

It uses `pure-python-adb` to interface with the ADB server.


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
- Update the frida-server `fah server update`: The latest Android frida-server is fetched from GitHub
release page using the GitHub API. This is then installed on the Android device using `fah server update` command.


### Android proxy configuration

- Enable proxy:
    - `fah proxy`: will automatically select an IP address from your PC, default port 8080
    - `fah proxy enable`: same as above
    - `fah proxy enable 192.168.137.137`: specify IP address, default port 8080
    - `fah proxy enable 192.168.137.137 8888`: specify IP address and port
- Disable proxy `fah proxy disable`
- Get current proxy settings `fah proxy get`


### Android screenshot
- `fah screen`: take a screenshot with the following format `deviceID_%Y.%m.%d_%H.%M.%S.png`
    - `fah screen filename`: take a screenshot with the following format: `deviceID_filename.png`


### Android disk snapshot
- `fah snap`: take a disk snapshot of the current open app
    - `fah snap com.example.app`: take a disk snapshot of `com.example.app` app


### Android certificate creation & installation for mitm purposes
- `fah cert`: generate a custom CA certificate to be imported in burp & device
    - `fah cert generate`: same as above
    - `fah cert install`: install specified certificate on device
    - `fah cert setup`: generate and install certificate (above commands combined)

### Android app
- `fah app`: try to download the currently opened app
    - `fah app dl`: same as above
    - `fah app dl com.example.app`: download com.example.app
- `fah app list`: list installed app on Android device.


### Android clipboard
- `fah clip`: display content of clipboard
    - `fah clip copy`: same as above
    - `fah clip paste foo bar`: set the content of the clipboard to `foo bar`


## Ideas & bugs
Ideas and bug reports are welcome! 
