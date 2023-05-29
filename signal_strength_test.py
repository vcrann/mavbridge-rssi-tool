import subprocess
import time
import argparse

parser = argparse.ArgumentParser(description="Display WLAN signal strength.")
parser.add_argument(
    dest="interface",
    nargs="?",
    default="wlx801f02f51f89",
    help="wlan interface (default: wlan0)",
)
args = parser.parse_args()

print("\n---Press CTRL+C to stop.---\n")

while True:
    cmd = subprocess.Popen(
        "iwconfig %s" % args.interface, shell=True, stdout=subprocess.PIPE
    )
    for line in cmd.stdout:
        if b"Link Quality" in line:
            output_strings = (
                line.lstrip(b" ")
                .decode("utf-8")
                .replace("Link Quality=", "")
                .replace("Signal level=", "")
                .replace(" dBm  ", "")
                .replace("\n", "")
                .split("  ")
            )
            print(output_strings)
            link_quality = output_strings[0]
            signal_level = output_strings[1]
        elif b"Not-Associated" in line:
            print("No signal")
    time.sleep(1)
