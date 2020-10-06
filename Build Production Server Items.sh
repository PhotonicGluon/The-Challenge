#!/bin/bash
# This file will run all the necessary commands to compile The-Challenge and to include all necessary files.
echo "Starting..."

# Config
export LANG=en_US.UTF-8
export LC_ALL=$LANG

# Constants
COMPRESSED_DIRECTORY_NAME="The-Challenge-Server-Items"

# Ensure that the current working directory is this script's directory
cd "$(dirname "$0")" || exit

# Create a "compilation" directory
mkdir "$COMPRESSED_DIRECTORY_NAME"

# Compile "The Challenge"
echo "Building The Challenge"
python setup.py bdist_wheel
echo "Built The Challenge"

# Move the generated build file to a separate directory
cd dist || exit

for entry in "."/*
do
  mv "$entry" ../"$COMPRESSED_DIRECTORY_NAME"
done

cd .. || exit

# Make a copy of the "Production Server Installation Instructions.txt" and "uWSGI_Configuration.ini" files
cp "Production Server Installation Instructions.txt" "$COMPRESSED_DIRECTORY_NAME"
cp "uWSGI_Configuration.ini" "$COMPRESSED_DIRECTORY_NAME"

# Get the current version of The Challenge
version=$(head -n 1 "VERSION")

# Compress all items inside the "$COMPRESSED_DIRECTORY_NAME" directory
echo
echo "Compressing files"
tar -czvf "The-Challenge-Production-Server_${version}.tar.gz" "$COMPRESSED_DIRECTORY_NAME"
echo "Done! You can find 'The-Challenge-Production-Server.tar.gz' in the current working directory."

# Delete temporary folders
rm -rf "$COMPRESSED_DIRECTORY_NAME"
rm -rf "dist"
rm -rf "build"
rm -rf "The_Challenge.egg-info"
