"""
obfuscateJSScripts.py

Created on 2020-10-10
Updated on 2020-11-08

Copyright Ryan Kan 2020

Description: Handles the obfuscation of the Javascript files.
"""

# IMPORTS
import os
from glob import glob


# FUNCTIONS
def obfuscate_js_script(path):
    """
    Obfuscates the javascript file at the path `path`.

    Args:
        path (str): Path to the javascript file.
    """
    os.system(f"javascript-obfuscator {path} --self-defending true --debug-protection true --split-strings true "
              f"--numbers-to-expressions true --disable-console-output true --dead-code-injection true "
              f"--string-array-encoding 'base64' --dead-code-injection-threshold 0.5 "
              f"--output {path[:-3] + '-obfuscated.js'}")


def get_all_files_to_obfuscate(base_path="the_challenge"):
    """
    Gets the paths of all the javascript files in the "the_challenge" directory that needs to be obfuscated.

    Args:
        base_path (str):    The path to the main folder, "the_challenge".

    Returns:
        List[str]:  Path of all the JavaScript files that are to be obfuscated.
    """

    # Iterate through every directory in the base path and find all files which ends in ".js"
    all_js_files = [f for f in glob(os.path.join(base_path, "**/*.js"), recursive=True)]

    # Exclude all javascript files which has ".min." in it (already obfuscated)
    files_to_be_obfuscated = []
    for file in all_js_files:
        if file.find(".min.") == -1:  # Not found
            files_to_be_obfuscated.append(file)

    # Return that list
    return sorted(files_to_be_obfuscated)


def obfuscate_js_files(base_path="the_challenge"):
    """
    Obfuscates the javascript files.

    Args:
        base_path (str):    The path to the main folder, "the_challenge".
                            (Default = "the_challenge")
    """

    # Get all needed javascript files
    files_to_be_obfuscated = get_all_files_to_obfuscate(base_path=base_path)

    # Iterate through every file
    for file in files_to_be_obfuscated:
        # Obfuscate the file
        obfuscate_js_script(file)

        # Rename the original file
        os.rename(file, file[:-3] + "_original.js")

        # Now rename the obfuscated file
        os.rename(file[:-3] + "-obfuscated.js", file)


def undo_obfuscation_renaming(base_path=".."):
    """
    Undoes the renaming of the original files (which occurred during obfuscation).

    Args:
        base_path (str):    The path to the main folder, "the_challenge".
                            (Default = "..")
    """

    # Get all javascript files
    all_js_files = [f for f in glob(os.path.join(base_path, "**/*.js"), recursive=True)]

    # Exclude all javascript files which has ".min." in it (already obfuscated) and split the remaining files into
    # different categories
    obfuscated_files = []
    original_files = []

    for file in all_js_files:
        if file.find(".min.") != -1:  # Is a vendor's file
            pass  # Skip that file
        elif file.find("_original.js") != -1:  # Is an original file
            original_files.append(file)
        else:  # The rest are (supposedly) obfuscated files
            obfuscated_files.append(file)

    # Delete the obfuscated files
    for file in obfuscated_files:
        os.remove(file)

    # Remove the "_original" string from the original files' names
    for file in original_files:
        os.rename(file, file.replace("_original", ""))


# DEBUG CODE
if __name__ == "__main__":
    obfuscate_js_files(base_path="..")
    undo_obfuscation_renaming(base_path="..")
