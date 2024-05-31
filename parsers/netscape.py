# Parsing code based off of https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser

from utils.classes import Bookmark, BookmarkFolder
import html
import re
import io
from typing import List

def parse_bookmark(tag: str) -> Bookmark:
    """Parses a bookmark tag from a Netscape bookmarks file.

    Args:
        tag: The HTML tag to parse.

    Returns:
        The parsed bookmark.
    """
    search = re.search(r'<DT><A HREF="(.*?)"(.*?)>(.*?)</A>', tag)
    url = search.group(1)
    name = html.unescape(search.group(3))
    bookmark = Bookmark(name, url)
    return bookmark

def parse_folder_tag(h3_tag: str, body: list) -> BookmarkFolder:
    """Parse a folder tag from a Netscape bookmarks file to recursively parse the bookmarks.

    Args:
        h3_tag: The HTML tag to parse.
        body: The body of the folder tag.

    Returns:
        The parsed folder.
    """
    name_escaped = re.search(r'<DT><H3(.*?)>(.*?)</H3>', h3_tag).group(2)
    name = html.unescape(name_escaped)
    bookmark_folder = BookmarkFolder(name)

    if len(body) != 0:
        i = 1

        while i < len(body):
            if '<DT><A' in body[i]:
                item = parse_bookmark(body[i])
                bookmark_folder.add_child(item)
            elif '<DT><H3' in body[i]:
                if '<DL><p>' not in body[i + 1]:
                    subfolder_empty = parse_folder_tag(h3_tag=body[i], body=[''])
                    bookmark_folder.add_child(subfolder_empty)
                    i += 1
                    continue

                elif '</DL><p>' in body[i + 2]:
                    subfolder_empty = parse_folder_tag(h3_tag=body[i], body=[''])
                    bookmark_folder.add_child(subfolder_empty)
                    i += 3
                    continue

                elif '</DL><p>' not in body[i + 2]:
                    body_start = i + 1
                    i += 2
                    tag_counter = 1
                    while tag_counter != 0 and i < len(body):
                        if '<DL><p>' in body[i]:
                            tag_counter += 1
                        if '</DL><p>' in body[i]:
                            tag_counter -= 1
                        if tag_counter == 0:
                            break
                        i += 1
                    body_end = i + 1
                    subfolder = parse_folder_tag(body[body_start - 1], body[body_start:body_end])
                    bookmark_folder.add_child(subfolder)
            i += 1

    return bookmark_folder

def parse(file: io.TextIOWrapper) -> List[Bookmark | BookmarkFolder]:
    """Parse a Netscape bookmarks file.

    Args:
        file: The file to parse.

    Returns:
        The parsed bookmarks.
    """
    line_num = 0
    lines = file.read().splitlines()

    while '<' not in lines[line_num]:
        line_num += 1

    while '<DL><p>' not in lines[line_num] and line_num < len(lines):
        line_num += 1

    body_start = line_num
    tag_counter = 0
    while line_num < len(lines):
        if '<DL><p>' in lines[line_num]:
            tag_counter += 1
        if '</DL><p>' in lines[line_num] or '</DL>' in lines[line_num]:
            tag_counter -= 1
        if tag_counter == 0:
            break
        line_num += 1
        
    body_end = line_num
    dummy_h3_tag = '<DT><H3>Bookmarks</H3>'
    parsed_bookmarks = parse_folder_tag(dummy_h3_tag, lines[body_start:body_end + 1])
    return [item for item in parsed_bookmarks.children]
