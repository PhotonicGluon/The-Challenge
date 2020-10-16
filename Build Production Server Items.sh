#!/bin/bash
#################################################################################
# Build Production Server Items.sh                                              #
#                                                                               #
# Created on 2020-09-21                                                         #
# Updated on 2020-10-16                                                         #
#                                                                               #
# Copyright Ryan Kan 2020                                                       #
#                                                                               #
# Description: A script that assists in building the files of The Challenge.    #
#################################################################################

# This file will run all the necessary commands to compile The-Challenge and to include all necessary files.
echo "Starting the build script..."

# Config
export LANG=en_US.UTF-8
export LC_ALL=$LANG

# Constants
COMPRESSED_DIRECTORY_NAME="The-Challenge-Server-Items"

# Ask user whether or not to obfuscate Javascript scripts
echo "'The Challenge' has an optional JavaScript Obfuscation System that can be activated."
echo "If you do want to use the JavaScript Obfuscation System, ensure that the instructions in 'Handle Obfuscator
Installation.txt' have been followed strictly."

while [ "$obfuscationAnswer" != "Y" ] && [ "$obfuscationAnswer" != "N" ] && [ "$obfuscationAnswer" != "y" ] && [ "$obfuscationAnswer" != "n" ]; do
    echo "Do you want to obfuscate the Javascript scripts in the production server?"
    echo "[Y]es or [N]o:"
    read -r obfuscationAnswer

    if [ "$obfuscationAnswer" != "Y" ] && [ "$obfuscationAnswer" != "N" ] && [ "$obfuscationAnswer" != "y" ] && [ "$obfuscationAnswer" != "n" ]; then
        echo "Please answer either 'Y' or 'N'."
        echo
    fi
done

# Ensure that the current working directory is this script's directory
cd "$(dirname "$0")" || exit 1

# Run obfuscation commands (if selected)
if [ "$obfuscationAnswer" = "Y" ] || [ "$obfuscationAnswer" = "y" ]; then
    # Obfuscate the files
    echo
    echo "Obfuscating JavaScript files..."
    python3 -c "import the_challenge; the_challenge.misc.obfuscate_js_files()"
    echo "Obfuscation procedure completed!"
fi

# Clear the dist directory
rm -rf "dist"

# Create a "compilation" directory
mkdir "$COMPRESSED_DIRECTORY_NAME"

# Compile "The Challenge"
echo
echo "Building The Challenge..."
python setup.py bdist_wheel
echo "Built The Challenge successfully."

# Undo the obfuscation (if selected)
if [ "$obfuscationAnswer" = "Y" ] || [ "$obfuscationAnswer" = "y" ]; then
    # Fix the names of the files
    echo
    echo "Undoing obfuscation renaming procedure..."
    python3 -c "import the_challenge; the_challenge.misc.undo_obfuscation_renaming()"
    echo "Done!"
fi

# Move the generated build file to a separate directory
cd dist || exit 1

for entry in "."/*; do
    mv "$entry" ../"$COMPRESSED_DIRECTORY_NAME"
done

cd .. || exit

# Make a copy of the "Production Server Installation Instructions.txt" and "uWSGI_Configuration.ini" files
cp "Production Server Installation Instructions.txt" "$COMPRESSED_DIRECTORY_NAME"
cp "uWSGI_Configuration.ini" "$COMPRESSED_DIRECTORY_NAME"

# Get the current version of The Challenge
version=$(python3 -c "import the_challenge;print(the_challenge.__version__)" | tail -n 1)

# Compress all items inside the "$COMPRESSED_DIRECTORY_NAME" directory
echo
echo "Compressing the generated files..."
tar -czvf "The-Challenge-Production-Server_${version}.tar.gz" "$COMPRESSED_DIRECTORY_NAME"

# Move generated tar file to the dist folder
mv "The-Challenge-Production-Server_${version}.tar.gz" "dist"
echo
echo "Done! The generated file can be found in the 'dist' folder."

# Delete temporary folders
rm -rf "$COMPRESSED_DIRECTORY_NAME"
rm -rf "build"
rm -rf "The_Challenge.egg-info"
