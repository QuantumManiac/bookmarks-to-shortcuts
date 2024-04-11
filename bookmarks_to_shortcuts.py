from typing import Dict, Any
import json
import os

def mirror_bookmarks(bookmarks: Dict[str, Any], output_folder: str):
    """Mirrors the Chrome bookmarks provided in the bookmarks dictionary to the output folder, converting bookmarks into internet shortcuts.

    Args:
        bookmarks: A dictionary containing the Chrome bookmarks.
        output_folder: The output folder to write the bookmarks to.
    """
    stack = [ (f"{output_folder}/{folder['name']}", folder) for folder in bookmarks["roots"].values()]
    while len(stack) > 0:
        folder_path, folder = stack.pop()
        for child in folder.get("children", []):
            if child["type"] == "folder":
                stack.append((f"{folder_path}/{child['name']}", child))
            elif child["type"] == "url":
                write_shortcut(child["name"], child["url"], folder_path)


def load_bookmarks(bookmarks_path: str) -> Dict[str, Any]:
    """Loads the Chrome bookmarks from the specified file.

    Args:
        bookmarks_path: The path to the Chrome bookmarks file.

    Returns:
        A dictionary containing the Chrome bookmarks.
    """
    try:
        with open(bookmarks_path, "r") as bookmarks_file:
            bookmarks = json.load(bookmarks_file)
            return bookmarks
    except FileNotFoundError:
        print(f"File not found: {bookmarks_path}")
        exit(1)

def write_shortcut(name: str, url: str, output_folder: str) -> str:
    """Writes an internet shortcut to the specified folder. Existing files will be overwritten.

    Args:
        name: The name of the shortcut.
        url: The URL of the shortcut.
        output_folder: The folder to write the shortcut to.

    Returns:
        The path to the written shortcut file.
    """
    # Fail if output_folder path length is too long
    if len(output_folder) > 255:
        print(f"Output folder path {output_folder} is too long.")
        exit(1)

    if name == '':
        name = "Untitled"
    else:
        # Replace any invalid characters in the name
        invalid_chars = "<>:\"/\\|?*"
        for char in invalid_chars:
            name = name.replace(char, "-")

    # Truncate the name if it's too long
    # output_folder + "/" + name + ".url" should be less than 255 characters
    expected_length = len(output_folder) + len(name) + 5
    if expected_length > 255:
        name = name[:255 - len(output_folder) - 5]

    path = os.path.join(output_folder, f"{name}.url")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(path, "w") as shortcut_file:
        shortcut_file.write("[InternetShortcut]\n")
        shortcut_file.write(f"URL={url}\n")

    return path
