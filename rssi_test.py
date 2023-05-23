import rssi_module.rssi as rssi
import time

interface = "wlx801f02f51f89"
rssi_scanner = rssi.RSSI_Scan(interface)

ssids = ["dd-wrt", "linksys"]

# sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# python file will have to be run with sudo privileges.
ap_info = rssi_scanner.getAPinfo(sudo=True)

print(ap_info[0]["signal"])

for x in range(20):
    ap_info = rssi_scanner.getAPinfo(sudo=True)
    print(ap_info[0]["signal"])
