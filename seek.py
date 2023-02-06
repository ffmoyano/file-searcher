from argparse import ArgumentParser
from pathlib import Path
import os


def filter_items(item: Path, remove_files: bool, remove_directory: bool, remove_hidden: bool, minimum_size: int,
                 maximum_size: int, substring: str) -> bool:
    valid_item: bool = True
    if remove_files and os.path.isfile(item):
        valid_item = False
    if remove_directory and os.path.isfile(item):
        valid_item = False
    if remove_hidden:
        if os.path.isfile(item) and item.name.startswith('.'):
            valid_item = False
    if minimum_size is not None and os.stat(item).st_size < minimum_size:
        valid_item = False
    if maximum_size is not None and maximum_size < os.stat(item).st_size:
        valid_item = False
    if substring is not None and substring not in item.name:
        valid_item = False
    return valid_item


def scan_folders(args: [any]):
    root_path = args.p if args.p else '.'
    path = Path(root_path)
    extension_pattern = '*.' + args.e if args.e else '*'
    items = path.glob(extension_pattern) if args.nr else path.rglob(extension_pattern)

    remove_files: bool = args.nf
    remove_directory: bool = args.nd
    remove_hidden: bool = args.nh
    minimum_size: int = args.m
    maximum_size: int = args.M
    substring: str = args.s

    print("{:<20} {:<10}".format('Size in Bytes', 'File'))
    for i in items:
        if filter_items(i, remove_files, remove_directory, remove_hidden, minimum_size, maximum_size, substring):
            size = os.stat(i).st_size
            file_path = os.path.abspath(i)
            print("{:<20} {:<10}".format(size, file_path))


def read_arguments() -> [any]:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-e', help='filter by file extension', metavar='extension', type=str)
    parser.add_argument('-m', help='minimum size of file in bytes', metavar='bytes', type=int)
    parser.add_argument('-M', help='maximum size of file in bytes', metavar='bytes', type=int)
    parser.add_argument('-nd', action='store_true', help='exclude directories from search')
    parser.add_argument('-nf', action='store_true', help='exclude files from search')
    parser.add_argument('-nh', action='store_true', help='exclude hidden files and directories from search')
    parser.add_argument('-nr', action='store_true', help='disables recursive search')
    parser.add_argument('-p', help='defines the root path which will be searched', metavar='path', type=str)
    parser.add_argument('-s', help='defines a string that must be contained by the file or directory name',
                        metavar='string', type=str)

    return parser.parse_args()


def main():
    args: [any] = read_arguments()
    scan_folders(args)


if __name__ == '__main__':
    main()
