"""
commandLine.py

Created on 2020-10-07
Updated on 2020-10-19

Copyright Ryan Kan 2020

Description: Contains all the command line commands that could be run.
"""

# IMPORTS
import argparse
import glob
import os
import shutil
import sys
from base64 import b64decode

import requests
import simplejson as json
from packaging import version

from the_challenge import __version__
from the_challenge.misc import check_token, get_most_recent_version, check_internet_connection


# FUNCTIONS
def update_the_challenge():
    """
    Updates the local copy of The Challenge.
    Usage: update_the_challenge [GITHUB_TOKEN]
    """

    # Form the parser
    parser = argparse.ArgumentParser(description="Updates The Challenge, when provided the valid access key.")
    parser.add_argument("access_token", type=str, help="The GitHub access token.")

    args = parser.parse_args()

    # Check if the user is online
    if not check_internet_connection():
        print("You are not connected to the internet. Try again later.")
        sys.exit()

    # Check the provided token
    access_token = args.access_token
    if not check_token(access_token):
        print("The provided token is not valid.")
        sys.exit()

    print("The provided token is valid.\nGetting most recent version...")

    # Get the GitHub version
    most_recent_version, most_recent_files = get_most_recent_version(access_token)

    # Get local version
    local_version = __version__

    # Check if local version is smaller than the GitHub version
    if version.parse(local_version) < version.parse(most_recent_version):
        print(f"There is a new version, {most_recent_version}, available.\n(Installed Version: {__version__})\n")

        while True:
            print("Do you want to update to the new version?")
            want_to_update = input("[Y]es or [N]o: ").upper()

            if want_to_update not in ["Y", "N"]:
                print("Please enter either 'Y' or 'N'.\n")
            elif want_to_update == "N":
                print("Keeping local version. Quitting now.")
                sys.exit()
            else:
                print("Starting update process...")
                break
    else:
        print("You are already on the latest version. Quitting now.")
        sys.exit()

    # Get the latest distribution file
    distribution_url = ""
    for file in most_recent_files:
        if file["path"].find("The-Challenge-Production-Server_") != -1:
            distribution_url = file["url"]
            break

    # Download the latest distribution
    if distribution_url != "":
        print("Downloading latest distribution...")
        download_request = requests.get(distribution_url, headers={"Authorization": "token %s" % access_token})
        download_request.raise_for_status()
        print("Done!")

        with open("./The-Challenge_Latest-Dist.tar.gz", "wb+") as f:
            f.write(b64decode(json.loads(download_request.text)["content"]))
            f.close()

    else:
        print("Can't get the latest distribution. Try again later.")
        sys.exit()

    # Extract the latest distribution
    print("Extracting contents of latest distribution...")
    shutil.unpack_archive("The-Challenge_Latest-Dist.tar.gz", "./extracted")
    os.remove("./The-Challenge_Latest-Dist.tar.gz")
    print("Done!")

    # Recursively try to find the wheel file in the extracted folder
    try:
        latest_wheel_file = [f for f in glob.glob("./extracted/" + "**/*.whl", recursive=True)][0]

        # Once found install it using pip
        os.system(f"pip install -U {latest_wheel_file}")

        print("The update was completed successfully.")

    except IndexError:
        print("The latest distribution file cannot be found. Quitting now...")
        sys.exit()

    # Clean up
    shutil.rmtree("./extracted")

    # Offer to automatically restart the service
    print()
    print("Only answer 'Y' to the following prompt if you (a) are on Ubuntu; (b) have a systemd service that "
          "hosts The Challenge's server; and (c) are an administrator that can use the 'sudo' command.")
    while True:
        print("Would you like to restart the systemd service?")
        confirm_systemd_name = input("[Y]es or [N]o: ").upper()

        if confirm_systemd_name not in ["Y", "N"]:
            print("Please enter either 'Y' or 'N'.\n")
        elif confirm_systemd_name == "N":
            print("Quitting now.")
            sys.exit()
        else:
            break

    # Ask user to input the systemd service name
    while True:
        print("Please enter the systemd service name.")
        systemd_service_name = input("?> ")

        if systemd_service_name == "":
            print("Please enter the name.")
        else:
            print("\nPlease confirm that you want to restart the systemd service named:")
            print(f"'{systemd_service_name}'")

            while True:
                confirm_systemd_name = input("[Y]es or [N]o: ").upper()

                if confirm_systemd_name not in ["Y", "N"]:
                    print("Please enter either 'Y' or 'N'.\n")
                    print("Please confirm the systemd service name.")
                elif confirm_systemd_name == "N":
                    print("Disregarding current input of the systemd service name.")
                    break
                else:
                    os.system(f"sudo systemctl restart {systemd_service_name}")
                    print("The systemd service has been restarted. Quitting.")
                    sys.exit()
