from argparse import ArgumentParser, Namespace
from pathlib import Path
import os


class Filters:
    extension: str
    minimum_size: int
    maximum_size: int
    non_recursive: bool
    path: str
    remove_files: bool
    remove_directory: bool
    remove_hidden: bool
    substring: str


def filter_items(item: Path, filters: Filters) -> bool:
    is_file: bool = os.path.isfile(item)
    item_size: int = os.stat(item).st_size
    if filters.remove_files and is_file:
        return False
    if filters.remove_directory and not is_file:
        return False
    if filters.remove_hidden:
        if item.name.startswith('.'):
            return False
        for i in item.parents:
            if i.name.startswith('.'):
                return False
    if filters.minimum_size is not None and item_size < filters.minimum_size:
        return False
    if filters.maximum_size is not None and filters.maximum_size < item_size:
        return False
    if filters.substring is not None and filters.substring not in item.name:
        return False
    return True


def scan_folders(filters: Filters):
    path: Path = Path(filters.path)
    items: [str] = path.glob(filters.extension) if filters.non_recursive else path.rglob(filters.extension)

    print("{:<20} {:<10}".format('Size in Bytes', 'File'))
    for i in items:
        if filter_items(i, filters):
            size = os.stat(i).st_size
            file_path = os.path.abspath(i)
            print("{:<20} {:<10}".format(size, file_path))


def read_arguments() -> Filters:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-e', help='filter by file extension', metavar='extension', type=str)
    parser.add_argument('-m', help='minimum size of file in bytes', metavar='bytes', type=int)
    parser.add_argument('-M', help='maximum size of file in bytes', metavar='bytes', type=int)
    parser.add_argument('-nd', action='store_true', help='exclude directories from search')
    parser.add_argument('-nf', action='store_true', help='exclude files from search')
    parser.add_argument('-nh', action='store_true', help='exclude hidden files and directories from search')
    parser.add_argument('-nr', action='store_true', help='disables recursive search')
    parser.add_argument('-p', help='defines the root path which will be searched. Defaults to script location', metavar='path', type=str)
    parser.add_argument('-s', help='defines a string that must be contained by the file or directory name',
                        metavar='string', type=str)

    args = parser.parse_args()

    filters: Filters = Filters()
    filters.extension = '*.' + args.e if args.e else '*'
    filters.minimum_size = args.m
    filters.maximum_size = args.M
    filters.non_recursive = args.nr
    filters.path = args.p if args.p else '.'
    filters.remove_directory = args.nd
    filters.remove_files = args.nf
    filters.remove_hidden = args.nh
    filters.substring = args.s

    return filters


def main():
    args: [any] = read_arguments()
    scan_folders(args)


if __name__ == '__main__':
    main()


