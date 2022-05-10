The scripts in this dir are intended for use on the host computer (windows) that the MacroPad is plugged into.

## `send_data_to_serial.py`
This script will compose a JSON string that contains some data and send it to the MacroPad. It uses a library for detecting the MacroPad which you will need to install. One of the datapoints it sends is the active window. This data is used on the MacroPad to drive what app is active and is powered by the script `getActiveWindowProcessName.ps1`. 

The script can be triggered in any way you see fit, I've included 2 options that are powered by Auto Hot Key:

1. `sendDataToSerial.ahk` works off of a hotkey (such as F13). You can use the MacroPad to trigger this, allowing the MacroPad to choose when it loads data from the host!
2. `activeWindowHook.py` uses Auto Hot Key to attach a hook in windows that will fire every time the active window changes. This will cause the MacroPad to be updated constantly.