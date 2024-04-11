import argparse
import os
from bookmarks_to_shortcuts import load_bookmarks, mirror_bookmarks

def main():
    parser = argparse.ArgumentParser(description="Mirrors Chrome bookmarks to your local filesystem, replicating the directory structure and converting bookmarks into internet shortcuts.")
    parser.add_argument("input", help="The input file to read bookmarks from.")
    parser.add_argument("-o", "--output", help="The output folder to write the bookmarks to. If not specified, the output folder will be the same as the input file.")
    args = parser.parse_args()

    bookmarks = load_bookmarks(args.input)

    output_folder = os.path.abspath(args.output) if args.output else os.path.dirname(os.path.abspath(args.input))

    mirror_bookmarks(bookmarks, output_folder)


if __name__ == "__main__":
    main()
    
