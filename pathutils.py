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

from pathlib import Path
from pprint import pprint as pp
from filecmp import cmp

ERROR_NOT_FILE = 'Error: Path is not file'
ERROR_NOT_PATH_OBJECT = 'Error: Path object required. Use create_path()'
SEARCH_PATTERN = '*'
ERROR_NOT_STRING = 'Error: arguments need to be strings'


def create_path(dir_str):
    path = Path(dir_str)
    return path


def build_helper(path):
    if not is_path(path):
        display_error(ERROR_NOT_PATH_OBJECT)
        return None

    path_dict = dict(path=path
                     , name=path.name
                     , stem=path.stem
                     , suffix=path.suffix
                     , parent=path.parent
                     , ptype=get_ptype(path)
                     , parts=get_parts(path)
                     , loc_files=get_local_files(path)
                     , loc_dirs=get_local_directories(path))
    return path_dict


def create_dir(dirname, dirlocation):

    if not is_path(dirname) and dirlocation is None:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None

    # combine the path parts to get a single path
    if is_string(dirname) and is_string(dirlocation):
        directory = combine_paths(dirlocation, dirname)

    # create directory object
    directory = create_path(directory)

    # make directory
    directory.mkdir(parents=True, exist_ok=True)

    return directory


def combine_paths(*dirs):
    path_str = ''
    for path in dirs:
        path_str += path + '/'
    return path_str


def create_local_dir(dir_name):
    dir_name = Path(Path.cwd() / dir_name)
    dir_name.mkdir(exist_ok=True)
    return dir_name


def is_path(obj):
    return isinstance(obj, Path)


def is_string(obj):
    return isinstance(obj, str)


def is_helper(path):
    return isinstance(path, dict)


def path_exists(path):
    if is_path(path):
        return path.exists()
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def is_dir(path):
    if is_path(path):
        return True if path.is_dir() else False
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def is_file(path):
    if is_path(path):
        return True if path.is_file() else False
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def display_error(error_msg):
    print(error_msg)


def get_component_folders(path):
    if is_path(path):
        return list([item for item in path.parts])


def get_ptype(path):
    if is_path(path):
        if is_dir(path):
            return 'directory'
        else:
            return 'file'
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def get_file_parent(path):
    if is_path(path):
        return path.parent
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def get_local_directories(path):
    if is_path(path):
        if is_dir(path):
            return list([item.name for item in path.iterdir() if item.is_dir()])
        else:
            parent = get_file_parent(path)
            return list([item.name for item in parent.iterdir() if item.is_dir()])

    display_error(ERROR_NOT_PATH_OBJECT)
    return None


def get_local_files(path):
    if is_path(path):
        if is_file(path):
            return list([item.name for item in path.iterdir() if item.is_file()])
        else:
            parent = get_file_parent(path)
            return list([item.name for item in parent.iterdir() if item.is_file()])
    display_error(ERROR_NOT_PATH_OBJECT)
    return None


def get_all_contents(path):
    if is_path(path):
        return list([item.name for item in path.rglob(SEARCH_PATTERN)])
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def get_parts(path):
    if is_path(path):
        return path.parts
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def set_ptype(path):
    if is_path(path):
        if is_dir(path):
            ptype = 'directory'
        else:
            ptype = 'file'
        return ptype
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def update_path(path):
    if is_path(path['path']):
        path['loc_files'] = get_local_files(path['path'])
        path['loc_dirs'] = get_local_directories(path['path'])
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


def list_all_files(path):
    if is_path(path):
        [print(item.name) for item in path.rglob(SEARCH_PATTERN) if item.is_file()]
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def list_all_directories(path):
    if is_path(path):
        [print(item.name) for item in path.rglob(SEARCH_PATTERN) if item.is_dir()]
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def list_all_contents(path):
    if is_path(path):
        [print(item.name) for item in path.rglob(SEARCH_PATTERN)]
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def list_local_files(path):
    if is_path(path):
        if is_file(path):
            [print(item.name) for item in path.iterdir() if item.is_file()]
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def list_local_dirs(path):
    if is_path(path):
        if is_file(path):
            [print(item.name) for item in path.iterdir() if item.is_dir()]
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def show_path_info(path):

    print(f"""Information: {path['path']}

    Path type: {path['ptype']}
    Name: {path['name']}
    File type: {path['suffix']}
    Local folders: {path['loc_dirs']}
    Local files: {path['loc_files']}
    """)
    print('\nAll Files:')
    list_all_files(path['path'])
    print('\nAll Folders:')
    list_all_directories(path['path'])
    print('\nDirectory Tree:')
    display_directory_tree(path['path'])


def get_helper_path(helper):
    return helper['path']
