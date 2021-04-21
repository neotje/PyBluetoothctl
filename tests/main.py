import bluetoothctl
import bluetooth

ctl = bluetoothctl.BluetoothCtl()

ctl.discoverable(True)

print("\npaired:")
for d in ctl.get_paired_devices():
    print(d)

print("\nscanning:")
for d in ctl.scan_for_devices(timeout=5):
    print(d)


device = bluetoothctl.BLdevice("04:F2:DD:C5:09:28", "OBDII")

print("\npairing:")
result = ctl.pair(device)
print(result)

print("\nconnecting:")
result = ctl.connect(device)
print(result)


device_name = "OBDII"

devices = bluetooth.discover_devices(lookup_names=True, duration=3)
print(f"Found {len(devices)} devices")

address = ""
for addr, name in devices:
    if name == device_name:
        address = addr
        break

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((address, 1))


print("\nremoving:")
ctl.remove(device)

