#!/bin/bash
# This file will run all the necessary commands to compile The-Challenge and to include all necessary files.
echo "Starting..."

# Config
export LANG=en_US.UTF-8
export LC_ALL=$LANG

# Constants
COMPRESSED_DIRECTORY_NAME="The Challenge Production Server Items"

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

# Compress all items inside "temp_compile"
echo
echo "Compressing files"
tar -czvf "The-Challenge-Production-Server.tar.gz" "$COMPRESSED_DIRECTORY_NAME"
echo "Done!"

# Delete the temporary folder
rm -rf "$COMPRESSED_DIRECTORY_NAME"
