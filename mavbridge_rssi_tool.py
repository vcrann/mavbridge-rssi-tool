#!/usr/bin/env python3
import subprocess
import argparse
import asyncio
import csv
import math
from datetime import datetime
from mavsdk import System


async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")
    position_ned = [0, 0, 0]
    # Start the tasks
    asyncio.ensure_future(get_position(drone, position_ned))

    # Get the interface as an argument
    parser = argparse.ArgumentParser(description="Display WLAN signal strength.")
    parser.add_argument(
        dest="interface",
        nargs="?",
        default="wlx801f02f51f89",
        help="wlan interface (default: wlan0)",
    )
    args = parser.parse_args()

    print("\n---Press CTRL+C to stop.---\n")

    experiment_name = input("Enter experiment name: ")
    file_name = datetime.now().strftime(
        "logs/" + experiment_name + "_" + "_log-%Y-%m-%d-%H-%M.csv"
    )
    with open(file_name, "a+") as f:
        writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_NONE)
        writer.writerow(
            (
                "time",
                "link_quality",
                "signal_level_dBm",
                "horizontal_distance_m",
                "straight_line_distance_m",
                "position_north_m",
                "position_east_m",
                "position_down_m",
            )
        )

        while True:
            link_quality, signal_level = get_link_quality(args)
            current_time = datetime.now().strftime("%H:%M:%S.csv")
            horizontal_distance = math.sqrt(position_ned[0] ** 2 + position_ned[1] ** 2)
            straight_line_distance = math.sqrt(
                position_ned[0] ** 2 + position_ned[1] ** 2 + position_ned[2] ** 2
            )
            writer.writerow(
                (
                    current_time,
                    link_quality,
                    signal_level,
                    horizontal_distance,
                    straight_line_distance,
                    position_ned[0],
                    position_ned[1],
                    position_ned[2],
                )
            )
            print(
                "Link Quality = {}, Signal Level = {}, Horizontal Distance = {}, Straight Line Distance = {}".format(
                    link_quality,
                    signal_level,
                    round(horizontal_distance, 3),
                    round(straight_line_distance, 3),
                )
            )
            await asyncio.sleep(1)


async def get_position(drone, position_ned):
    async for position_velocity_ned in drone.telemetry.position_velocity_ned():
        # print(position_velocity_ned.position)
        position_ned[0] = position_velocity_ned.position.north_m
        position_ned[1] = position_velocity_ned.position.east_m
        position_ned[2] = position_velocity_ned.position.down_m


def get_link_quality(args):
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
            link_quality = output_strings[0]
            signal_level = output_strings[1]
        elif b"Not-Associated" in line:
            print("No signal")
            link_quality = "0"
            signal_level = "0"
    return link_quality, signal_level


if __name__ == "__main__":
    asyncio.ensure_future(run())
    event_loop = asyncio.get_event_loop()
    event_loop.run_forever()
