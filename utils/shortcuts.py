from typing import List

from utils.classes import Bookmark, BookmarkFolder
import os


def write_shortcut(bookmark: Bookmark, output_folder: str) -> str:
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

    name = bookmark.title

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
        shortcut_file.write(f"URL={bookmark.url}\n")

    return path

def create_shortcuts(bookmarks: List[Bookmark | BookmarkFolder], output_folder: str):
    """Creates internet shortcuts from the bookmarks and writes them to the output folder.

    Args:
        bookmarks: The bookmarks to create shortcuts from.
        output_folder: The folder to write the shortcuts to.
    """
    for item in bookmarks:
        match item:
            case Bookmark():
                write_shortcut(item, output_folder)
            case BookmarkFolder():
                create_shortcuts(item.children, os.path.join(output_folder, item.title))
