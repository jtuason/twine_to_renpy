# Twine to Ren'Py

The Twine to Ren'Py tool allows you to write a simple Ren'Py game but with the visual outlining of writing in Twine. Convert a Sugarcube Twine html file into rpy files for your Ren'Py game project.

This requires Python 2.7 to run. If you don't have it, you can download the application here:
https://ludowoods.itch.io/twine-to-renpy-tool

## Features:

- Converts Twine-like choices into Ren'Py menus
- Converts Twine variables and conditionals to Ren'Py
(Note that conditional results need to be on a new line to be processed properly. See demo Twine file uploaded as of 7/3)
- Option to define characters and variables at start of script
- Replaces special characters and passage titles with Ren'Py safe terms
- Add custom replacement terms
- Use passage tags to break up into separate rpy files
- Includes Sugarcube demo for writing Ren'Py games in Twine

## How to run Python script:
1. Download the directory
2. Open the cmd prompt in the twine_to_renpy directory
3. Run python twine_to_rpy.py

## How to run the pyinstaller exe from the itch page:

1. Unzip the directory
2. Run twine_to_rpy.exe inside the twine_to_rpy directory
2. Select the html file (Demo.html is included for testing) and directory to output rpy files
4. Run!

## Curious how to set up your Twine file?

Open the Demo.html in Twine 2 to see how the file is written for tool processing.

## Run into a bug?

Drop the steps to reproduce the bug in the itch comments.

# Suggestions?

This tool won't be closely supported in the future, but if you have a suggestion for a feature that would help you with a project feel free to let me know in the itch comments or add yourself.