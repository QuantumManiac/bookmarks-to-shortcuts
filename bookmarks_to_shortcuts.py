from utils.enums import BookmarkFileFormat
from parsers.chromium import parse as parse_chromium
from parsers.netscape import parse as parse_netscape
from utils.shortcuts import create_shortcuts

from typing import List
from utils.classes import Bookmark, BookmarkFolder

def mirror_bookmarks(bookmarks_path: str, output_folder: str, format: BookmarkFileFormat):
    """Mirrors the Chrome bookmarks provided in the bookmarks file to the output folder, converting bookmarks into internet shortcuts.

    Args:
        bookmarks_path: The path to the bookmarks file.
        output_folder: The output folder to write the bookmarks to.
    """

    bookmarks = parse_bookmarks(bookmarks_path, format)
    create_shortcuts(bookmarks, output_folder)

def parse_bookmarks(bookmarks_path: str, bookmarks_format) -> List[Bookmark | BookmarkFolder]:
    """Parse the bookmarks file.

    Args:
        bookmarks_path: The path to the bookmarks file.

    Returns:
        The parsed bookmarks.
    """
    try:
        with open(bookmarks_path, "r", encoding="utf-8") as bookmarks_file:
            match bookmarks_format:
                case BookmarkFileFormat.CHROMIUM:
                    bookmarks = parse_chromium(bookmarks_file)
                case BookmarkFileFormat.NETSCAPE:
                    bookmarks = parse_netscape(bookmarks_file)
                case _:
                    raise NotImplementedError(f"Unsupported bookmarks format: {bookmarks_format}")
            return bookmarks
    except FileNotFoundError:
        print(f"File not found: {bookmarks_path}")
        exit(1)
