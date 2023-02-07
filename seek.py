from argparse import ArgumentParser
from pathlib import Path
import os


class Filters:
    extension: str
    minimumsize: int
    maximumsize: int
    nondirectories: bool
    nonfiles: bool
    nonhidden: bool
    nonrecursive: bool
    path: str
    substring: str

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            if k == 'extension':
                setattr(self, k, '*.' + v if v else '*')
            elif k == 'path':
                setattr(self, k, v if v else '.')
            else:
                setattr(self, k, v)


def filter_items(item: Path, filters: Filters) -> bool:
    is_file: bool = os.path.isfile(item)
    item_size: int = os.stat(item).st_size
    if filters.nondirectories and not is_file:
        return False
    if filters.nonfiles and is_file:
        return False
    if filters.nonhidden:
        if item.name.startswith('.'):
            return False
        for i in item.parents:
            if i.name.startswith('.'):
                return False
    if filters.minimumsize is not None and item_size < filters.minimumsize:
        return False
    if filters.maximumsize is not None and filters.maximumsize < item_size:
        return False
    if filters.substring is not None and filters.substring not in item.name:
        return False
    return True


def scan_folders(filters: Filters):
    path: Path = Path(filters.path)
    items: [str] = path.glob(filters.extension) if filters.nonrecursive else path.rglob(filters.extension)

    print("{:<20} {:<10}".format('Size in Bytes', 'File'))
    for i in items:
        if filter_items(i, filters):
            size = os.stat(i).st_size
            file_path = os.path.abspath(i)
            print("{:<20} {:<10}".format(size, file_path))


def read_arguments() -> Filters:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-e', '--extension', help='filter by file extension', metavar='extension', type=str)
    parser.add_argument('-m', '--minimumsize', help='minimum size of file in bytes', metavar='bytes', type=int)
    parser.add_argument('-M', '--maximumsize', help='maximum size of file in bytes', metavar='bytes', type=int)
    parser.add_argument('-nd', '--nondirectories', action='store_true', help='exclude directories from search')
    parser.add_argument('-nf', '--nonfiles', action='store_true', help='exclude files from search')
    parser.add_argument('-nh', '--nonhidden', action='store_true',
                        help='exclude hidden files and directories from search')
    parser.add_argument('-nr', '--nonrecursive', action='store_true', help='disables recursive search')
    parser.add_argument('-p', '--path',
                        help='defines the root path which will be searched. Defaults to script location',
                        metavar='path', type=str)
    parser.add_argument('-s', '--substring',
                        help='defines a string that must be contained by the file or directory name',
                        metavar='string', type=str)

    args = vars(parser.parse_args())
    filters: Filters = Filters(args)

    return filters


def main():
    args: [any] = read_arguments()
    scan_folders(args)


if __name__ == '__main__':
    main()
