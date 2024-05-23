import argparse
import os
from bookmarks_to_shortcuts import load_bookmarks, mirror_bookmarks

def main():
    parser = argparse.ArgumentParser(description="Mirrors browser bookmarks to your local filesystem, replicating the directory structure and converting bookmarks into internet shortcuts.")
    parser.add_argument("input", help="The input file to read bookmarks from.")
    parser.add_argument("-f", "--format", choices=["chromium", "netscape"], help="The format of the input file. Can either be the Chromium Bookmarks file or a Netscape Bookmark File. If not specified, the format will be inferred from the file extension.")
    parser.add_argument("-o", "--output", help="The output folder to write the bookmarks to. If not specified, the output folder will be the current working directory.")
    args = parser.parse_args()

    # If format is not specified, infer it from the file extension
    if not args.format:
        _, ext = os.path.splitext(args.input)
        if ext == ".html":
            args.format = "netscape"
            print("file extension is html. Assuming this is a Netscape Bookmark File")
        else:
            args.format = "chromium"
            print("file extension is not html. Assuming this is a Chromium Bookmarks file")

    bookmarks = load_bookmarks(args.input)

    # By default, the output folder is the current working directory
    output_folder = os.path.abspath(args.output) if args.output else os.getcwd()

    mirror_bookmarks(bookmarks, output_folder)


if __name__ == "__main__":
    main()
    
