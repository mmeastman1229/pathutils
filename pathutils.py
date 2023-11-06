#!/usr/bin/env python

"""Pathutils

This script allows the user to utilize pathlib functions for the purpose
of checking and manipulating files and folders. The purpose is to be
able to pass pathlib objects around with proper validation while easily
getting and setting the desired objects throughout any program utilizing
Path objects.

Path must be imported from the pathlib

After a path is created, all ite components will be added to namedtuple
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
COLLECTION_TYPE = 'namedtuple'


PHelper = namedtuple('PHelper', [
            'self'
            ,'exists'
            ,'is_dir'
            ,'is_file'
            ,'parts'
            ,'drive'
            ,'root'
            ,'anchor'
            ,'parents'
            ,'parent'
            ,'name'
            ,'suffix'
            ,'suffixes'
            ,'stem'
            ,'cwd'
            ,'home'
            ,'stats'
            ,'link_stats'
            ,'as_posix'
            ,'as_uri'
            ,'get_owner'
            ,'expanduser'
            ,'is_absolute'
            ,'is_reserved'
            ,'is_block_device'
            ,'is_char_device'
            ,'is_fifo'
            ,'is_mount'
            ,'is_socket'
            ,'is_symlink'
            ,'get_linkk'
            ,'hardlink_to'
            ,'symlink_to'
            ,'unlink'
            ,'resolve'
            ,'joinpath'
            ,'match'
            ,'iterdir'
            ,'glob'
            ,'rglob'
            ,'group'
            ,'change_name'
            ,'change_name_and_type'
            ,'change_type'
            ,'make_absolute'
            ,'change_mode'
            ,'change_link_mode'
            ,'mkdir'
            ,'rmdir'
            ,'open'
            ,'touch'
            ,'write_bytes'
            ,'write_text'
            ,'read_bytes'
            ,'read_text'
            ,'relative_to'
            ,'rename'
            ,'replace'
            ,'samefile'
            ,'ptype'
            ,'info'
            ,'display_tree'
            ,'dir_contents'
            ,'subdirs'
            ,'all_contents'
            ,'local_dirs'
            ,'local_files'
            ,'nested_dirs'
            ,'nested_files'
            ,'lfile_total'
            ,'nfile_total'
            ,'ndir_total'
            ,'ldir_total'
        ])


def create_path(directory):
    return Path(directory)


def create_helper(path):

    path = PHelper(
          self=path
        , exists=path.exists()
        , is_dir=path.is_dir()
        , is_file=path.is_file()
        , parts=path.parts
        , drive=path.drive
        , root=path.root
        , anchor=path.anchor
        , parents=list(path.parents)
        , parent=path.parent
        , name=path.name
        , suffix=path.suffix
        , suffixes=path.suffixes
        , stem=path.stem
        , cwd=path.cwd()
        , home=path.home()
        , stats=path.stat  # returns a stat() object
        , link_stats=path.lstat
        , as_posix=path.as_posix
        , as_uri=path.as_uri
        , get_owner=path.owner
        , expanduser=path.expanduser
        , is_absolute=path.is_absolute()
        , is_reserved=path.is_reserved`
        , is_block_device=path.is_block_device()
        , is_char_device=path.is_char_device()
        , is_fifo=path.is_fifo()
        , is_mount=path.is_mount
        , is_socket=path.is_socket()
        , is_symlink=path.is_symlink()
        , get_linkk=path.readlink
        , hardlink_to=path.hardlink_to
        , symlink_to=path.symlink_to
        , unlink=path.unlink
        , resolve=path.resolve
        , joinpath=path.joinpath
        , match=path.match
        , iterdir=path.iterdir
        , glob=path.glob
        , rglob=path.rglob
        , group=path.group
        , change_name=path.with_stem
        , change_name_and_type=path.with_name
        , change_type=path.with_suffix
        , make_absolute=path.absolute
        , change_mode=path.chmod
        , change_link_mode=path.lchmod
        , mkdir=path.mkdir
        , rmdir=path.rmdir
        , open=path.open
        , touch=path.touch
        , write_bytes=path.write_bytes
        , write_text=path.write_text
        , read_bytes=path.read_bytes
        , read_text=path.read_text
        , relative_to=path.relative_to
        , rename=path.rename
        , replace=path.replace
        , samefile=path.samefile

        # my custom functions
        , ptype=get_ptype(path)
        , info=show_path_info
        , display_tree=display_directory_tree
        , dir_contents=get_all_contents(path)
        , subdirs=get_subdirs
        , all_contents=get_all_contents(path)
        , local_dirs=get_ldirs(path)
        , local_files=get_lfiles(path)
        , nested_dirs=get_ndirs(path)
        , nested_files=get_nfiles(path)
        , lfile_total=get_lfile_total(path)
        , nfile_total=get_nfiles_total(path)
        , ndir_total=get_ndir_total(path)
        , ldir_total=get_ldir_total(path)
    )
    return path

def is_path(obj):
    return isinstance(obj, Path)


def is_string(obj):
    return isinstance(obj, str)


def is_collection(path, collection_type):
    return isinstance(path, collection_type)


def get_nondunder_fields(collection):
    return [field for field in dir(collection) if not field.startswith('__')]


def get_all_fields(collection):
    return [field for field in collection._fields]


def get_collection_type_path(collection):
    return collection.path if is_collection(collection)


def get_obj_type(obj):
    return type(obj)


# local file functions
def get_lfiles(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    return ([item.name for item in path.iterdir() if item.is_file()])


def get_ldirs(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    return [item.name for item in path.iterdir() if item.is_dir()]


def get_lfile_total(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    return len([item for item in path.iterdir() if item.is_file()])


def list_local_files(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    [print(item.name) for item in path.iterdir() if item.is_file()]
    return None


# local folders


def get_ldir_total(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    return len([item for item in path.iterdir() if item.is_dir()])


def list_local_subdirs(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    [print(item.name) for item in path.iterdir() if item.is_dir()]
    return None


# nested file functions
def get_nfiles(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    return [item.name for item in path.rglob(SEARCH_PATTERN) if item.is_file()]


def get_nfiles_total(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    return len([item for item in path.rglob(SEARCH_PATTERN) if item.is_file()])


def list_all_files(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    [print(item.name) for item in path.rglob(SEARCH_PATTERN) if item.is_file()]
    return None


# Nested Subdirs
def get_ndirs(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    return [item.name for item in path.rglob(SEARCH_PATTERN) if item.is_dir()]


def get_ndirs_total(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    return len([item for item in path.rglob(SEARCH_PATTERN) if item.is_dir()])


def list_nested_subdirs(path):
    if is_collection(path):
        path = get_collection_type_path(path)

    [print(item.name) for item in path.rglob(SEARCH_PATTERN) if item.is_dir()]
    return None


def get_local_totals(path):
    files = 0
    dirs = 0
    for item in path.iterdir():
        if path.is_dir():
            dirs += 1
        else:
            files += 1
    return files, dirs


def get_nested_totals(path):
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




def display_msg(error_msg):
    print(error_msg)


def get_path_parts(path):
    return path.parts


def get_nested_dirs(path):
    return [item.name for item in path.rglob(SEARCH_PATTERN) if item.is_dir()]


def get_nfiles(path):
    return [item.name for item in path.rglob(SEARCH_PATTERN) if item.is_file()]



def create_dir(name):
    name = Path(Path.cwd() / name)
    return name.mkdir(exist_ok=True)


def update_path(path):
    if is_path(path['path']):
        path['loc_files'] = get_lfiles(path['path'])
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
    print(f"""Information:            {collection.path}
    Path exists:                      {collection.exists}
    Path type:                        {collection.ptype}
    Name:                             {collection.name}
    File type:                        {collection.suffix}
    Directory parts:                  {collection.parts}
    Local file count:                 {collection.lfile_total}
    Local directory count:            {collection.total_local_dirs}
    Total file counts:                {collection.total_files}
    Total directory counts:           {collection.ldir_total}
    """)

    if collection.ptype == 'directory':

        print("\n\t\t\t\tLocal Folders: \n")
        collection.get_ldirs(collection.path)

        print("\n\t\t\t\tLocal Files: \n")
        collection.get_lfiles(collection.path)

        print("\n\t\t\t\tAll Files: \n")
        collection.get_nfiles(collection.path)

        print("\n\t\t\t\tAll Folders: \n")
        collection.get_ndirs(collection.path)

    print("\n\t\t\t\t Directory Tree: \n")
    collection.display_directory_tree(collection.path)
