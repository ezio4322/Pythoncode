import argparse
import os
import shutil

FILE_SUBPARSER = 'file'
DIR_SUBPARSER = 'directory'

parser = argparse.ArgumentParser(prog='client',
                                 description='This program is used for XYZ...')

subparsers = parser.add_subparsers(help='File operations', dest='subparser_name')
# This is where you add a subparser
file_subparser = subparsers.add_parser(name=FILE_SUBPARSER, help='Handle file operations')
# TODO: add an arg parser for directories

# This is where you add arguments
file_subparser.add_argument('--source', dest='source_data', action='store', required=True,
                            help='Path to the input file/directory')
file_subparser.add_argument('--create', dest='create_data', action='store',
                            help='Create file at input path')
file_subparser.add_argument('--read', dest='read_data', action='store',
                            help='Read file at input path')
file_subparser.add_argument('--update', dest='update_data', action='store',
                            help='Update file at input path')
file_subparser.add_argument('--delete', dest='delete_data', action='store',
                            help='Delete file at input path')

dir_subparser = subparsers.add_parser(name=DIR_SUBPARSER, help='Handle directory operations')

dir_subparser.add_argument('--source', dest='source_data', action='store', required=True,
                           help='Path to the input directory')
dir_subparser.add_argument('--create', dest='create_flag', action='store_true',
                           help='Create directory at input path')
dir_subparser.add_argument('--read', dest='read_flag', action='store_true',
                           help='Read file at input path')
dir_subparser.add_argument('--delete', dest='delete_flag', action='store_true',
                           help='Delete directory at input path')
# TODO: add the rest of the arguments


def file_op_handler(arg: argparse.Namespace):
    # this is the field where your input data is stored
    if arg.create_data:
        create_file(arg)
    if arg.read_data:
        read_file(arg)
    if arg.update_data:
        update_file(arg)
    if arg.delete_data:
        delete_file(arg)


def create_file(arg: argparse.Namespace):
    print('creating file')
    if os.path.exists(arg.source_data + '/' + arg.create_data):
        print('File/directory with same name already exists')
    else:
        p_list = arg.source_data.split('/')
        p_path = p_list[0]
        i = 0
        while i < len(p_list) - 1:
            if os.path.isdir(p_path + '/' + p_list[i + 1]):
                i += 1
                p_path += '/' + p_list[i]
            else:
                break
        while i < len(p_list) - 1:
            i += 1
            p_path += '/' + p_list[i]
            os.mkdir(p_path)
        p_path += '/' + arg.create_data
        with open(p_path, mode='w'):
            print('Successfully created file')


def read_file(arg: argparse.Namespace):
    print('reading file')
    if os.path.isfile(arg.source_data):
        with open(arg.source_data, mode='rb') as f:
            b_str = f.read(int(arg.read_data))
        print(b_str)
    else:
        print('no file at input path')


def update_file(arg: argparse.Namespace):
    print('updating file')
    if os.path.isfile(arg.source_data):
        with open(arg.source_data, mode='a') as f:
            f.write(arg.update_data)
    else:
        print('no file at input path')


def delete_file(arg: argparse.Namespace):
    print('deleting file')
    if os.path.isfile(arg.source_data + '/' + arg.delete_data):
        os.remove(arg.source_data + '/' + arg.delete_data)
        print('deleted')
    else:
        print('no file at input path')


def dir_op_handler(arg: argparse.Namespace):
    if arg.create_flag:
        create_dir(arg)
    if arg.read_flag:
        read_dir(arg)
    if arg.delete_flag:
        delete_dir(arg)


def create_dir(arg: argparse.Namespace):
    print('creating directory')
    if os.path.exists(arg.source_data):
        print('File/directory with same name already exists')
    else:
        p_list = arg.source_data.split('/')
        p_path = p_list[0]
        i = 0
        while i < len(p_list) - 1:
            if os.path.isdir(p_path + '/' + p_list[i + 1]):
                i += 1
                p_path += '/' + p_list[i]
            else:
                break
        while i < len(p_list) - 1:
            i += 1
            p_path += '/' + p_list[i]
            os.mkdir(p_path)
        print('Successfully created directory')


def read_dir(arg: argparse.Namespace):
    print('reading directory')
    if os.path.isdir(arg.source_data):
        if os.listdir(arg.source_data):
            print('directory contains these entities')
            print(os.listdir(arg.source_data))
        else:
            print('directory is empty')
    else:
        print('no directory at input path')


def delete_dir(arg: argparse.Namespace):
    print('deleting directory')
    if os.path.isdir(arg.source_data):
        if os.listdir(arg.source_data):
            print('directory not empty, entities inside: ')
            print(os.listdir(arg.source_data))
            shutil.rmtree(arg.source_data)
            print('directory deleted and entities deleted')
        else:
            print('directory is empty')
            os.rmdir(arg.source_data)
            print('directory deleted')

    else:
        print('no directory at input path')


if __name__ == '__main__':
    # TODO: implement operations like create, read, update, delete
    args = parser.parse_args()
    if args.subparser_name == FILE_SUBPARSER:
        file_op_handler(args)
    else:
        if args.subparser_name == DIR_SUBPARSER:
            dir_op_handler(args)
        else:
            print('file/directory only')


# Command looks something like this

# python3 PJ.py file --source /home/cosmin/test --create tst.txt
# python3 PJ.py file --source /home/cosmin/test/crazy/hamburger --create tst.txt
# python3 PJ.py file --source /home/cosmin/test/words.txt --read 1000
# python3 PJ.py file --source /home/cosmin/test/words.txt --update hamburger
# python3 PJ.py file --source /home/cosmin/test --delete whatever.txt

# python3 PJ.py directory --source /home/cosmin/test/burger --create
# python3 PJ.py directory --source /home/cosmin/test --read
# python3 PJ.py directory --source /home/cosmin/test/burger --delete
