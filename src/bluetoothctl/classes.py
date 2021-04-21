import pexpect
import subprocess
import sys
import time
from typing import List
from bluetoothctl.exceptions import BluetoothctlError


class BLdevice:
    mac: str = None
    name: str = None

    def __init__(self, mac: str = None, name: str = None):
        self.mac = mac
        self.name = name

    def __repr__(self) -> str:
        return f"mac: {self.mac} name: {self.name}"


class BluetoothCtl:
    def __init__(self):
        self._device = "bluetooth"

        disconnect = subprocess.run(["bluetoothctl", "disconnect"]) 

        self._ctl = pexpect.spawn("bluetoothctl", echo=False, encoding="utf-8")
        pass

    def _execute(self, cmd: str, timeout: float = None) -> str:
        self._ctl.send(f"{cmd}\n")

        if not timeout == None:
            time.sleep(timeout)

        # check if command failed
        failed = self._ctl.expect([self._device, "bluetooth", pexpect.EOF])
        if failed == 2:
            raise BluetoothctlError(f"Failed after running: {cmd}")

        return self._ctl.before

    def _parse_device(self, info_string: str) -> BLdevice:
        d = BLdevice()

        # block lines who don't contain any device info
        block_list = ["[\x1b[0;", "removed"]
        valid = not any(keyword in info_string for keyword in block_list)

        if valid:
            try:
                # second check if line contains any device info
                d_pos = info_string.index("Device")
            except ValueError:
                pass
            else:
                if d_pos > -1:
                    parts = info_string.split(" ")
                    d.mac = parts[1].strip()
                    d.name = " ".join(parts[2:]).strip()

                    return d

    def _to_list(self, text: str) -> List[BLdevice]:
        arr = []

        for l in text.splitlines():
            d = self._parse_device(l)
            if d:
                arr.append(d)

        return arr

    def get_paired_devices(self) -> List[BLdevice]:
        result = self._execute("paired-devices")

        return self._to_list(result)

    def scan_for_devices(self, timeout=5, ignore_paired: bool = True) -> List[BLdevice]:
        self._execute("scan on", timeout)

        arr = self._to_list(
            self._execute("devices")
        )

        if ignore_paired:
            paired = self.get_paired_devices()
            to_remove = []

            for d in arr:
                for p in paired:
                    if d.mac == p.mac:
                        to_remove.append(d)

            for r in to_remove:
                try:
                    arr.remove(r)
                except ValueError:
                    pass

        return arr

    def discoverable(self, enable: bool = True):
        if enable:
            cmd = "discoverable on"
        else:
            cmd = "discoverable off"

        try:
            self._execute(cmd)
        except BluetoothctlError as e:
            print(e)
            return

    def pair(self, device: BLdevice, pin: str = "1234") -> bool:
        self._ctl.send(f"pair {device.mac}\n")

        """while True:
                out = self._ctl.readline()
                print(out.replace("\n", ""))

            time.sleep(3)"""

        status = self._ctl.expect(["PIN", "confirmation", "Failed", "successful"])
        print(status)

        if status == 0:
            time.sleep(0.1)
            self._ctl.send(f"{pin}\n")
        elif status == 1:
            self._ctl.send("yes\n")
        elif status == 2:
            print("device may already be paired.")
            return False
        elif status == 3:
            return True

        failed = self._ctl.expect(["bluetooth", device.name, pexpect.EOF])
        if failed == 2:
            return False
        return True

    def connect(self, device: BLdevice, timeout: float = -1) -> bool:
        self._ctl.send(f"connect {device.mac}\n")

        failed = self._ctl.expect(["successful", "Failed"], timeout=timeout)
        if failed:
            print("connection failed. Are you paired with this device? Are you near the device?")
            return False

        self._device = device.name
        return True

    def remove(self, device: BLdevice):
        try:
            self._execute(f"remove {device.mac}")
        except BluetoothctlError as e:
            print(e)
            return
