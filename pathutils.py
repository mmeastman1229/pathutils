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


def create_helper_item_collection(path):
    
    lfiles, ldirs = get_local_counts(path)
    nfiles, ndirs = get_nested_counts(path)

    properties_and_methods = dict(
        # Main Path object info
        path=path
        , keys=None
        , name=path.name 
        , exists=path.exists()
        , is_dir=path.is_dir()
        , is_file=path.is_file()
        , ptype=get_ptype(path)
        , home=path.home()
        , cwd=path.cwd()
        , is_absolute=path.is_absolute()
        , parents=list(path.parents)
        , root=path.root
        , drive=path.drive
        , anchor=path.anchor # combination of root and drive
        , stem=path.stem  # name of file without suffix
        , suffix=path.suffix
        , suffixes=path.suffixes
        , parts=path.parts
        
        # Files and Folder Info
        , subdirs=get_subdirs(path)
        , files=get_files(path)
        , all_files=get_nested_files(path)
        , all_dirs=get_nested_subdirs(path)
        , dir_contents=get_all_contents(path)
        , total_local_files=lfiles
        , total_local_dirs=ldirs
        , total_files=nfiles
        , total_subdirs=ndirs
        
        # Other useful functions
        , join=path.joinpath
        , rename_file=path.with_stem
        , change_type=path.with_suffix
        , change_name_and_type=path.with_name
        , read_text=path.read_text
        , read_bytes=path.read_bytes
        , display_tree=display_directory_tree
        , info=show_path_info
        )
    
    properties_and_methods['keys'] = get_keys(properties_and_methods)
    return properties_and_methods


def get_keys(collection):
    return [key for key in collection]


def get_collection_path(path):
    return path['path']


# local file functions
def get_files(path):
    if is_collection(path):
        path = get_collection_path(path)
    
    return ([item.name for item in path.iterdir() if item.is_file()])
    

def get_file_count(path):
    if is_collection(path):
        path = get_collection_path(path)

    return len([item for item in path.iterdir() if item.is_file()])


def list_files(path):
    if is_collection(path):
        path = get_collection_path(path)

    [print(item.name) for item in path.iterdir() if item.is_file()]
    return None


# local folders
def get_subdirs(path):
    if is_collection(path):
        path = get_collection_path(path)

    return [item.name for item in path.iterdir() if item.is_dir()]


def get_subdir_count(path):
    if is_collection(path):
        path = get_collection_path(path)
    
    return len([item for item in path.iterdir() if item.is_dir()])


def list_subdirs(path):
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


def list_keys(path_dict):
    [print(key) for keys in path_dict]

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


def is_dict(path):
    return isinstance(path, dict)


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


def list_all_contents(path):
    if is_path(path):
        [print(item.name) for item in path.rglob(SEARCH_PATTERN)]
    else:
        display_error(ERROR_NOT_PATH_OBJECT)
        return None


def show_path_info(path):
    print(f"""Information:            {path['path']}
    Path exists:                      {path['exists']}
    Path type:                        {path['ptype']}
    Name:                             {path['name']}
    File type:                        {path['suffix']} 
    Directory parts:                  {path['parts']}
    Local file count:                 {path['total_local_files']}
    Local directory count:            {path['total_local_dirs']}
    Total file counts:                {path['total_files']}
    Total directory counts:           {path['total_subdirs']} 
    """)
   
    if path['ptype'] == 'directory':

        print("\n\t\t\t\tLocal Folders: \n")
        list_subdirs(path)
        
        print("\n\t\t\t\tLocal Files: \n")
        list_files(path)
        
        print("\n\t\t\t\tAll Files: \n")
        list_all_files(path)
        
        print("\n\t\t\t\tAll Folders: \n")
        list_nested_subdirs(path)
        
    print("\n\t\t\t\t Directory Tree: \n")
    display_directory_tree(path)


def get_helper_path(helper):
    return helper['path']


def get_helper_exists(helper):
    return helper['exists']
