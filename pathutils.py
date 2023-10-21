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

def create_path(directory):
    return Path(directory)


def create_path_property_collection(path):

    path_properties = dict(
        path=path
        , drive=path.drive
        , root=path.root
        , anchor=path.anchor
        , parents=list(path.parents)
        , name=path.name
        , suffix=path.suffix
        , suffixes=path.suffixes
        , stem=path.stem)
    
    return path_dict


def create_path_fn_collection(path):
    path_functions = dict(
        , cwd=path.cwd()
        , home=path.home()
        , is_dir=path.is_dir()
        , is_file=path.is_file()
        , change_type=path.with_suffix
        , change_filename=path.with_stem
        , read_text=path.read_text)

    return path_functions




def add_collection_property(collection):
    pass



def add_collection_function(collection)
    pass
  
  if not is_dict(collection):
      display_error(ERROR_NOT_PATH_DICT)
      return None
  
  if collection['is_dir']:
    collection['ptype'] = 'directory'
    collection['files'] = get_files(collection)
    
    
    collection['nested_files'] = get_nested_files(path)
    collection['nested_dirs'] = get_nested_directories(path)
    collection['all_dirs_subs'] = get_all_directories(path)
    collection['all_dir_sub_files'] = get_all_files(path)
    collection['contents'] = get_all_contents(path)
    collection['local_type_counts'] = c(p.suffix for p in path.iterdir())
    collection['all_type_counts'] = c(p.suffix for p in path.rglob('*'))
        
    if path_dict['ptype'] == 'file':
        path_dict['suffix'] = path.suffix


def create_subdirectory(dirname, dirlocation):

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


def create_dir(name):
    name = Path(Path.cwd() / name)
    return name.mkdir(exist_ok=True) 


def is_path(obj):
    return isinstance(obj, Path)


def is_string(obj):
    return isinstance(obj, str)


def is_dict(path):
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


def get_subdirectories(path):
    if is_path(path):
        if is_dir(path):
            return list([item.name for item in path.iterdir() if item.is_dir()])
        else:
            parent = get_file_parent(path)
            return list([item.name for item in parent.iterdir() if item.is_dir()])

    display_error(ERROR_NOT_PATH_OBJECT)
    return None


def get_files(path):
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
    Path exists: {path['does_exist']}
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


def get_helper_exists(helper):
    return helper['exists']
