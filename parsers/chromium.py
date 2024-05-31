import json
import io

from utils.classes import Bookmark, BookmarkFolder

from typing import List

def parse(file: io.TextIOWrapper) -> List[Bookmark | BookmarkFolder]:
    res = []

    bookmarks_data = json.loads(file.read())

    for item in bookmarks_data["roots"].values():
        res.append(parse_item(item))

    return res

def parse_item(item: dict) -> Bookmark | BookmarkFolder:
    if item["type"] == "url":
        return Bookmark(item["name"], item["url"])
    elif item["type"] == "folder":
        folder = BookmarkFolder(item["name"])
        for child in item.get("children", []):
            folder.add_child(parse_item(child))
        return folder
