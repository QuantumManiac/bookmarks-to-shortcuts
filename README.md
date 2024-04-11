# bookmarks-to-shortcuts
Mirrors Chrome bookmarks to your local filesystem, replicating the directory structure and converting bookmarks into internet shortcuts.

## Usage

This script takes the Bookmarks file that Chromium-based browsers use to store bookmarks as the input. Typically, this file is:
```sh
"%appdata%\Local\Google\Chrome\User Data\Default\Bookmarks" # Windows
"~/.config/google-chrome/Default/Bookmarks" # Linux
"~/Library/Application Support/Google/Chrome/Default/Bookmarks" # MacOS
```
The filepath may vary depending on the user profile that you're not using in the browser (i.e. not Default). Other Chromium-based browsers should store their bookmarks in a similar location.

As for usage of the script itself:
```
❯ python main.py -h
usage: main.py [-h] [-o OUTPUT] input

Mirrors Chrome bookmarks to your local filesystem, replicating the directory structure and converting bookmarks into internet shortcuts.

positional arguments:
  input                 The input file to read bookmarks from.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The output folder to write the bookmarks to. If not specified, the output folder will be the same as the folder containing the input file.
```
