import argparse
import os
import shutil
import time

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
file_subparser.add_argument('--create', dest='create_flag', action='store_true',
                            help='Create file at input path')
file_subparser.add_argument('--read', dest='read_data', action='store',
                            help='Read file at input path')
file_subparser.add_argument('--update', dest='update_data', action='store',
                            help='Update file at input path')
file_subparser.add_argument('--search', dest='search_data', action='store',
                            help='Search for file at input path')
file_subparser.add_argument('--info', dest='info_flag', action='store_true',
                            help='Information of file at input path')
file_subparser.add_argument('--copy', dest='copy_data', action='store',
                            help='Copy file at input path')
file_subparser.add_argument('--hardlink', dest='hardlink_data', action='store',
                            help='Hard-linking file at input path')
file_subparser.add_argument('--delete', dest='delete_flag', action='store_true',
                            help='Delete file at input path')

dir_subparser = subparsers.add_parser(name=DIR_SUBPARSER, help='Handle directory operations')

dir_subparser.add_argument('--source', dest='source_data', action='store', required=True,
                           help='Path to the input directory')
dir_subparser.add_argument('--create', dest='create_flag', action='store_true',
                           help='Create directory at input path')
dir_subparser.add_argument('--read', dest='read_flag', action='store_true',
                           help='Read file at input path')
dir_subparser.add_argument('--search', dest='search_data', action='store',
                           help='Search for directory at input path')
dir_subparser.add_argument('--info', dest='info_flag', action='store_true',
                           help='Information of directory at input path')
dir_subparser.add_argument('--delete', dest='delete_flag', action='store_true',
                           help='Delete directory at input path')
# TODO: add the rest of the arguments


def file_op_handler(arg: argparse.Namespace):
    # this is the field where your input data is stored
    if arg.create_flag:
        create_file(arg)
    if arg.read_data:
        read_file(arg)
    if arg.update_data:
        update_file(arg)
    if arg.search_data:
        search_file(arg)
    if arg.info_flag:
        info_file(arg)
    if arg.copy_data:
        copy_file(arg)
    if arg.hardlink_data:
        hardlink_file(arg)
    if arg.delete_flag:
        delete_file(arg)


def create_file(arg: argparse.Namespace):
    print('creating file')
    if os.path.exists(arg.source_data):
        print('file/directory with same name already exists')
    else:
        p_path, f_name = os.path.split(arg.source_data)
        os.makedirs(p_path, exist_ok=True)
        p_path = os.path.join(p_path, f_name)
        with open(p_path, mode='w'):
            print('successfully created file')


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


def search_file(arg: argparse.Namespace):
    print('searching file')
    if not os.path.isdir(arg.source_data):
        print('no directory at input path')
        return
    print('directory exists, searching for file')
    p_list = []
    for d_path, dir_list, file_list in os.walk(arg.source_data):
        if arg.search_data in file_list:
            p_list.append(os.path.join(d_path, arg.search_data))
    if not p_list:
        print('no file found')
        return
    print('there were ', len(p_list), ' instance(s) with file name:', arg.search_data)
    for i in p_list:
        print(i)


def info_file(arg: argparse.Namespace):
    print('info file')
    if os.path.isfile(arg.source_data):
        stat_l = os.stat(arg.source_data)
        print('size of file: ', stat_l.st_size, 'bytes')
        print('creation date of file: ', time.asctime(time.localtime(stat_l.st_ctime)))
        print('last modification date of file: ', time.asctime(time.localtime(stat_l.st_mtime)))
        print('number of inodes: ', stat_l.st_ino)
        print('number of hardlinks: ', stat_l.st_nlink)
    else:
        print('no file at input path')


def copy_file(arg: argparse.Namespace):
    print('copying file')
    if os.path.isfile(arg.source_data):
        if os.path.isdir(arg.copy_data):
            p_split = os.path.split(arg.source_data)
            p_path = os.path.join(arg.copy_data, p_split[1])
            if os.path.exists(p_path):
                print('file/directory with same name already exists')
            else:
                if not os.path.isdir(arg.copy_data):
                    os.makedirs(arg.copy_data)
                with open(p_path, mode='w'):
                    print('file created')
            shutil.copyfile(arg.source_data, p_path)
            print('successfully copied file')
        else:
            print('no directory at input path')
    else:
        print('no file at input path')


def hardlink_file(arg: argparse.Namespace):
    print('hard-linking file')
    if os.path.isfile(arg.source_data):
        if not (os.path.exists(arg.hardlink_data)):
            os.link(arg.source_data, arg.hardlink_data)
            print('successfully hard-linked file')
        else:
            print('file/directory with same name exists at input path')
    else:
        print('no file at input path')


def delete_file(arg: argparse.Namespace):
    print('deleting file')
    if os.path.isfile(arg.source_data):
        os.remove(arg.source_data)
        print('deleted')
    else:
        print('no file at input path')


def dir_op_handler(arg: argparse.Namespace):
    if arg.create_flag:
        create_dir(arg)
    if arg.read_flag:
        read_dir(arg)
    if arg.search_data:
        search_dir(arg)
    if arg.info_flag:
        info_dir(arg)
    if arg.delete_flag:
        delete_dir(arg)


def create_dir(arg: argparse.Namespace):
    print('creating directory')
    if os.path.exists(arg.source_data):
        print('file/directory with same name already exists')
    else:
        os.makedirs(arg.source_data)
        print('successfully created directory')


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


def search_dir(arg: argparse.Namespace):
    print('searching directory')
    if not os.path.isdir(arg.source_data):
        print('no directory at input path')
        return
    print('directory exists, searching for directory')
    p_list = []
    for d_path, dir_list, file_list in os.walk(arg.source_data):
        if arg.search_data in dir_list:
            p_list.append(os.path.join(d_path, arg.search_data))
    if not p_list:
        print('no directory found')
        return
    print('there were ', len(p_list), ' instance(s) with directory name:', arg.search_data)
    for i in p_list:
        print(i)


def info_dir(arg: argparse.Namespace):
    print('info directory')
    if os.path.isdir(arg.source_data):
        f_number = 0
        d_number = 0
        d_size = 0
        for d_path, dir_list, file_list in os.walk(arg.source_data):
            for i in file_list:
                f_number += 1
                d_size += os.path.getsize(os.path.join(d_path, i))
            for i in dir_list:
                d_number += 1
        print('the directory size is:', d_size, ' bytes')
        print('the directory has:', f_number, ' files')
        print('the directory has:', d_number, ' directories')
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

# python3 PJ.py file --source /home/cosmin/test/tst.txt --create
# python3 PJ.py file --source /home/cosmin/test/crazy/hamburger/tst.txt --create
# python3 PJ.py file --source /home/cosmin/test/words.txt --read 1000
# python3 PJ.py file --source /home/cosmin/test/words.txt --update hamburger
# python3 PJ.py file --source /home/cosmin/test/whatever.txt --delete

# python3 PJ.py directory --source /home/cosmin/test/burger --create
# python3 PJ.py directory --source /home/cosmin/test --read
# python3 PJ.py directory --source /home/cosmin/test/burger --delete

# python3 PJ.py file --source /home/cosmin/test --search text.txt
# python3 PJ.py file --source /home/cosmin/test/text.txt --info
# python3 PJ.py file --source /home/cosmin/test/text.txt --copy /home/cosmin/test/dir69
# python3 PJ.py file --source /home/cosmin/test/text.txt --hardlink /home/cosmin/test/hard_dir

# python3 PJ.py directory --source /home/cosmin/test --search dir
# python3 PJ.py directory --source /home/cosmin/test --info
