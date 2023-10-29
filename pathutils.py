#!/usr/bin/env python

"""Pathutils

This script allows the user to utilize pathlib functions for the purpose
of checking and manipulating files and folders. The purpose is to be
able to pass pathlib objects around with proper validation while easily
getting and setting the desired objects throughout any program utilizing
Path objects.

Path must be imported from the pathlib

After a path is created, all ite components will be added to dictionary
for easy access.


common argument names:
path: directory of the file or folder as a path object and not a string
directory: a Path created for purpose of being directory only, not a file
file: a Path created for purpose of being a file
ptype = path type (file or directory)


When importing the file, alias the the library as "putil"
"""

from collections import Counter
from collections import namedtuple
from filecmp import cmp
from pathlib import Path
from pprint import pprint


ERROR_NOT_FILE = 'ERROR: Not a file.'
ERROR_NOT_PATH_OBJECT = 'Use create_path("/directory/to/file/or/folder") ' \
    'or pass Path object directly to function .'
ERROR_NOT_STRING = 'ERROR: arguments need to be strings'
ERROR_DOES_NOT_EXIST = 'ERROR: Path does not exist. ' \
                        'Use create_path() to utilize function'
ERROR_NOT_PATH_DICT = 'ERROR: Not a dictionary. ' \
                    'Run create_path_item_collection(path) to utilize function'
SEARCH_PATTERN = '*'


PHelper = namedtuple('PHelper', [
                        'absolute',
                        'all_dirs',
                        'all_files',
                        'anchor',
                        'as_posix',
                        'as_uri',
                        'change_name',
                        'change_name_and_type',
                        'change_type',
                        'chmod',
                        'cwd',
                        'dir_contents',
                        'display_tree',
                        'drive',
                        'exists',
                        'expanduser',
                        'files',
                        'glob',
                        'group',
                        'hardlink_to',
                        'home',
                        'info',
                        'is_absolute',
                        'is_block_device',
                        'is_char_device',
                        'is_dir',
                        'is_fifo',
                        'is_file',
                        'is_mount',
                        'is_relative_to',
                        'is_reserved',
                        'is_socket',
                        'is_symlink',
                        'iterdir',
                        'joinpath',
                        'lchmod',
                        'link_to',
                        'lstat',
                        'match',
                        'mkdir',
                        'name',
                        'ndirs',
                        'nfiles',
                        'open',
                        'owner',
                        'parent',
                        'parents',
                        'parts',
                        'path',
                        'ptype'
                        'read_bytes',
                        'read_text',
                        'readlink',
                        'relative_to',
                        'rename',
                        'replace',
                        'resolve',
                        'rglob',
                        'rmdir',
                        'root',
                        'samefile',
                        'stat',
                        'stem',
                        'subdirs'
                        'suffix',
                        'suffixes',
                        'symlink_to',
                        'total_lf_cnt',
                        'total_nf_cnt',
                        'total_nsdir_cnt'
                        'total_subdir_cnt',
                        'touch',
                        'unlink',
                        'write_bytes',
                        'write_text'])


def create_path(directory):
    return Path(directory)


def create_helper(path):

    path = PHelper(
             absolute=path.absolute(),
             all_dirs=get_nested_subdirs,
             all_files=get_nested_files,
             anchor=path.anchor,
             as_posix=path.as_posix,
             as_uri=path.as_uri,
             change_name=path.with_stem,
             change_name_and_type=path.withname,
             change_type=path.with_suffix,
             chmod=path.chmod,
             cwd=path.cwd(),
             dir_contents=get_all_contents,
             display_tree=display_directory_tree,
             drive=path.drive,
             exists=path.exists(),
             expanduser=path.expanduser,
             files=get_files,
             glob=path.glob,
             group=path.group,
             hardlink_to=path.hardlink_to,
             home=path.home(),
             info=show_path_info,
             is_absolute=path.is_absolute(),
             is_block_device=path.is_block_device(),
             is_char_device=path.is_char_device(),
             is_dir=path.is_dir(),
             is_fifo=path.is_fifo(),
             is_file=path.is_file(),
             is_mount=path.is_mount,
             is_relative_to=path.is_relative_to,
             is_reserved=path.is_reserved(),
             is_socket=path.is_socket(),
             is_symlink=path.is_symlink(),
             iterdir=path.iterdir,
             joinpath=path.joinpath,
             lchmod=path.lchmod,
             link_to=path.link_to,
             lstat=path.lstat,
             match=path.match,
             mkdir=path.mkdir,
             name=path.name,
             ndirs=get_nested_subdirs,
             nfiles=get_nested_files,
             open=path.open,
             owner=path.owner,
             parent=path.parent,
             parents=list(path.parents),
             parts=path.parts,
             path=path,
             ptype=get_ptype(path),
             read_bytes=path.read_bytes,
             read_text=path.read_text,
             readlink=path.readlink,
             relative_to=path.relative_to,
             rename=path.rename,
             replace=path.replace,
             resolve=path.resolve,
             rglob=path.rglob,
             rmdir=path.rmdir,
             root=path.root,
             samefile=path.samefile,
             stat=path.stat,
             stem=path.stem,
             subdirs=get_subdirs,
             suffix=path.suffix,
             suffixes=path.suffixes,
             symlink_to=path.symlink_to,
             total_lf_cnt=get_file_count(path),
             total_nf_cnt=get_nested_subdir_count(path),
             total_nsdir_cnt= get_nested_subdir_count(path),
             total_subdir_cnt=ldirs,
             touch=path.touch,
             unlink=path.unlink,
             write_bytes=path.write_bytes,
             write_text=path.write_text)
    return path


def get_fields(collection):
    return [field for field in collection._fields]


def get_collection_path(collection):
    return collection.path if is_collection(collection)


# local file functions
def get_local_files(path):
    if is_collection(path):
        path = get_collection_path(path)

    return ([item.name for item in path.iterdir() if item.is_file()])


def get_local_file_count(path):
    if is_collection(path):
        path = get_collection_path(path)

    return len([item for item in path.iterdir() if item.is_file()])


def list_local_files(path):
    if is_collection(path):
        path = get_collection_path(path)

    [print(item.name) for item in path.iterdir() if item.is_file()]
    return None


# local folders
def get_local_subdirs(path):
    if is_collection(path):
        path = get_collection_path(path)

    return [item.name for item in path.iterdir() if item.is_dir()]


def get_local_subdir_count(path):
    if is_collection(path):
        path = get_collection_path(path)

    return len([item for item in path.iterdir() if item.is_dir()])


def list_local_subdirs(path):
    if is_collection(path):
        path = get_collection_path(path)

    [print(item.name) for item in path.iterdir() if item.is_dir()]
    return None


# nested file functions
def get_nested_files(path):
    if is_collection(path):
        path = get_collection_path(path)

    return [item.name for item in path.rglob(SEARCH_PATTERN) if item.is_file()]


def get_total_file_count(path):
    if is_collection(path):
        path = get_collection_path(path)

    return len([item for item in path.rglob(SEARCH_PATTERN) if item.is_file()])


def list_all_files(path):
    if is_collection(path):
        path = get_collection_path(path)

    [print(item.name) for item in path.rglob(SEARCH_PATTERN) if item.is_file()]
    return None


# Nested Subdirs
def get_nested_subdirs(path):
    if is_collection(path):
        path = get_collection_path(path)

    return [item.name for item in path.rglob(SEARCH_PATTERN) if item.is_dir()]


def get_nested_subdir_count(path):
    if is_collection(path):
        path = get_collection_path(path)

    return len([item for item in path.rglob(SEARCH_PATTERN) if item.is_dir()])


def list_nested_subdirs(path):
    if is_collection(path):
        path = get_collection_path(path)

    [print(item.name) for item in path.rglob(SEARCH_PATTERN) if item.is_dir()]
    return None


def get_local_counts(path):
    files = 0
    dirs = 0
    for item in path.iterdir():
        if path.is_dir():
            dirs += 1
        else:
            files += 1
    return files, dirs


def get_nested_counts(path):
    files = 0
    dirs = 0
    for item in path.rglob(SEARCH_PATTERN):
        if path.is_dir():
            dirs += 1
        else:
            files += 1
    return files, dirs


def create_subdir(dirname, dirlocation):

    # combine the path parts to get a single path
    if is_string(dirname) and is_string(dirlocation):
      directory = combine_paths(dirlocation, dirname)

    # create directory object
    directory = create_path(directory)

    # make directory
    directory.mkdir(parents=True, exist_ok=True)

    return directory


def combine_paths(path):
    Path.join(path)


def create_dir(name):
    name = Path(Path.cwd() / name)
    return name.mkdir(exist_ok=True)


def is_path(obj):
    return isinstance(obj, Path)


def is_string(obj):
    return isinstance(obj, str)


def is_collection(path):
    return isinstance(path, namedtuple)


def display_msg(error_msg):
    print(error_msg)


def get_path_parts(path):
    return path.parts


def get_nested_dirs(path):
    return [item.name for item in path.rglob(SEARCH_PATTERN) if item.is_dir()]


def get_nested_files(path):
    return [item.name for item in path.rglob(SEARCH_PATTERN) if item.is_file()]



def create_dir(name):
    name = Path(Path.cwd() / name)
    return name.mkdir(exist_ok=True)


def update_path(path):
    if is_path(path['path']):
        path['loc_files'] = get_local_files(path['path'])
        path['loc_dirs'] = get_local_directories(path['path'])
        path['does_exist'] = path_exists(path['path'])
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def display_directory_tree(directory):
    if is_path(directory):
        if is_dir(directory):
            path = directory
        else:
            path = directory.parent
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None

    print(f'+ {path}')
    for path_item in sorted(path.rglob(SEARCH_PATTERN)):
        depth = len(path_item.relative_to(path).parts)
        spacer = '   ' * depth
        print(f'{spacer}+ {path_item.name}')


def display_contents(contents):
    for item in sorted(contents):
        print(item)


def list_all_contents(path):
    if is_path(path):
        [print(item.name) for item in path.rglob(SEARCH_PATTERN)]
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def show_path_info(collection):
    print(f"""Information:            {path.path}
    Path exists:                      {path.exists}
    Path type:                        {path.ptype}
    Name:                             {path.name}
    File type:                        {path.suffix}
    Directory parts:                  {path.parts}
    Local file count:                 {path.total_local_files}
    Local directory count:            {path.total_local_dirs}
    Total file counts:                {path.total_files}
    Total directory counts:           {path.total_subdirs}
    """)

    if collection.ptype == 'directory':

        print("\n\t\t\t\tLocal Folders: \n")
        collection.get_local_subdirs(collection.path)

        print("\n\t\t\t\tLocal Files: \n")
        collection.get_local_files(collection.path)

        print("\n\t\t\t\tAll Files: \n")
        collection.get_nested_files(collection.path)

        print("\n\t\t\t\tAll Folders: \n")
        collection.get_nested_subdirs(collection.path)

    print("\n\t\t\t\t Directory Tree: \n")
    collection.display_directory_tree(collection.path)
