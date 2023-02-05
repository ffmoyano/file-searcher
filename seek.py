from argparse import ArgumentParser
from os import walk


def read_arguments():
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-e', help='filter by file extension', metavar='extension', type=str)
    parser.add_argument('-m', help='minimum size of file in bytes', metavar='bytes', type=int)
    parser.add_argument('-M', help='maximum size of file in bytes', metavar='bytes', type=int)
    parser.add_argument('-nd', action='store_true', help='exclude directories from search')
    parser.add_argument('-nf', action='store_true', help='exclude files from search')
    parser.add_argument('-nh', action='store_true', help='exclude hidden files and directories from search')
    parser.add_argument('-p', help='defines the root path which will be searched', metavar='path', type=str)
    parser.add_argument('-r', action='store_true', help='tells the program to search recursively')
    parser.add_argument('-s', help='defines a string that must be contained by the file or directory name',
                        metavar='string', type=str)

    return parser.parse_args()


def main():
    args= read_arguments()
    print(args)


if __name__ == '__main__':
    main()
