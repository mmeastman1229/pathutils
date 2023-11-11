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


def is_path(obj):
    return isinstance(obj, Path)


def is_string(obj):
    return isinstance(obj, str)


def is_collection(collection, collection_type):
    return isinstance(collection, collection_type)


def is_phelper(path):
    return isinstance(path, namedtuple)


def path_exists(path):
    return path.exists


def is_dir(path):
    return path.is_dir


def is_file(path):
    return path.is_file


PHelper = namedtuple('PHelper', [
            'path'
            , 'exists'
            , 'is_dir'
            , 'is_file'
            , 'parts'
            , 'drive'
            , 'root'
            , 'anchor'
            , 'parents'
            , 'parent'
            , 'name'
            , 'suffix'
            , 'suffixes'
            , 'stem'
            , 'cwd'
            , 'home'
            , 'stats'
            , 'link_stats'
            , 'as_posix'
            , 'as_uri'
            , 'get_owner'
            , 'expanduser'
            , 'is_absolute'
            , 'is_reserved'
            , 'is_block_device'
            , 'is_char_device'
            , 'is_fifo'
            , 'is_mount'
            , 'is_socket'
            , 'is_symlink'
            , 'get_linkk'
            , 'hardlink_to'
            , 'symlink_to'
            , 'unlink'
            , 'resolve'
            , 'joinpath'
            , 'match'
            , 'iterdir'
            , 'glob'
            , 'rglob'
            , 'group'
            , 'change_name'
            , 'change_name_and_type'
            , 'change_type'
            , 'make_absolute'
            , 'change_mode'
            , 'change_link_mode'
            , 'mkdir'
            , 'rmdir'
            , 'open'
            , 'touch'
            , 'write_bytes'
            , 'write_text'
            , 'read_bytes'
            , 'read_text'
            , 'relative_to'
            , 'rename'
            , 'replace'
            , 'samefile'
            , 'ptype'
            , 'info'
            , 'display_tree'
            , 'tree_items'
            , 'root_dirs'
            , 'root_files'
            , 'subdirs'
            , 'subdir_files'
            , 'rootfile_cnt'
            , 'rootdir_cnt'
            , 'subdir_cnt'
            , 'subdir_file_cnt'
        ])


def create_helper(path):

    path = PHelper(
         path=path
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
        , is_reserved=path.is_reserved
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
        , ptype=_get_ptype(path)
        , info=show_path_info
        , display_tree=display_tree
        , tree_items=_get_tree_items
        , root_dirs=_get_root_dirs
        , root_files=_get_root_files
        , subdirs=_get_subdirs
        , subdir_files=_get_subdir_files
        , rootfile_cnt=_get_rootfiles_cnt
        , rootdir_cnt=_get_rootdirs_cnt
        , subdir_cnt=_get_subdirs_cnt
        , subdir_file_cnt=_get_subdirfiles_cnt
    )

    return path


def get_nondunder_fields(collection):
    return [field for field in dir(collection) if not field.startswith('__')]



def get_all_fields(collection):
    return [field for field in collection._fields]



def get_obj_type(obj):
    return type(obj)



def get_path(collection):
    return collection.path



def get_parts(path):
    return path.parts



def get_subdir_cnt(path):
    return len(path.nested_dirs)



def create_path(directory):
    return Path(directory)



def create_dir(name):
    name = Path(Path.cwd() / name)
    return name.mkdir(exist_ok=True)


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


def _get_ptype(collection):
    return 'directory' if collection.is_dir() else 'file'



def _get_root_dirs(path):
    return list([item for item in path.iterdir() if item.is_dir()])



def _get_root_files(path):
    return list([item for item in path.iterdir() if item.is_file()])



def _get_subdirs(path):
    return list([item for item in path.rglob(SEARCH_PATTERN) if item.is_dir()])



def _get_subdir_files(path):
    return list([item for item in path.rglob(SEARCH_PATTERN) if item.is_file()])



def _get_tree_items(path):
    return list([item for item in path.rglob(SEARCH_PATTERN)])


def _get_rootfiles_cnt(path):
    return len([item for item in path.iterdir() if item.is_file()])


def _get_rootdirs_cnt(path):
    return len([item for item in path.iterdir() if item.is_dir()])


def _get_subdirs_cnt(path):
    return len([item for item in path.rglob(SEARCH_PATTERN) if item.is_dir()])


def _get_subdirfiles_cnt(path):
    return len([item for item in path.rglob(SEARCH_PATTERN) if item.is_file()])



def _get_treeitems_cnt(path):
    return len([item for item in path.glob(SEARCH_PATTERN)])


def create_folder_structure(path):
    for folder_number, folder in enumerate(path.parents):
        print(f'folder-{folder_number} is {folder}' )


def display_msg(msg):
    print(msg)



def display_tree(directory):
    if directory.is_dir:
        path = directory
    else:
        path = directory.parent

    print(f'+ {path}')
    for path_item in sorted(path.rglob(SEARCH_PATTERN)):
        depth = len(path_item.relative_to(path).parts)
        spacer = '   ' * depth
        print(f'{spacer}+ {path_item.name}')


def list_subdir_files(phelper):
   for file in phelper.subdir_files(phelper.path):
       print(file.name)


def list_subdirs(phelper):
    for directory in phelper.subdirs(phelper.path):
        print(directory.name)


def list_all_contents(phelper):
    for item in phelper.tree_items(phelper.path):
        print(item.name)


def list_root_files(phelper):
    for file in phelper.root_files(phelper.path):
        print(file.name)


def list_root_dirs(phelper):
    for directory in phelper.root_dirs(phelper.path):
        print(directory.name)


def show_path_info(phelper):
    print(f"""Information:      {phelper.path}
    Path exists:                {phelper.exists}
    Path type:                  {phelper.ptype}
    Name:                       {phelper.name}
    File type:                  {phelper.suffix}
    Directory parts:            {phelper.parts}
    Local file count:           {phelper.rootfile_cnt(phelper.path)}
    Local directory count:      {phelper.rootdir_cnt(phelper.path)}
    Total file counts:          {phelper.subdir_file_cnt(phelper.path)}
    Total directory counts:     {phelper.subdir_cnt(phelper.path)}
    """)

    if phelper.ptype == 'directory':

        print("\n\t\t\t\tLocal Folders: \n")
        list_root_dirs(phelper)

        print("\n\t\t\t\tLocal Files: \n")
        list_root_files(phelper)

        print("\n\t\t\t\tAll Files: \n")
        list_subdir_files(phelper)

        print("\n\t\t\t\tAll Folders: \n")
        list_subdirs(phelper)

    print("\n\t\t\t Directory Tree: \n")
    phelper.display_tree(phelper.path)


def bulk_name_change(phelper, old_str, new_str):
    directory = phelper.path
    pattern = f'*{old_str}*'
    matching_files = directory.rglob(pattern)

    for path in matching_files:
        new_name = path.name.replace(old_str, new_str)
        path.rename(path.with_name(new_name))


def find_duplicates(lst):
    unique_set = set()
    duplicates = set()
    dup_info = {}

    for item in lst:
        if item in unique_set:
            duplicate.add(item)
        else:
            unique_set.add(item)

    return duplicates


def get_file_types(path):
    file_types = set()
    for file in path:
        file_types.add(file.suffix)
    return file_types


def file_check(file1, file2):
    return cmp(file1, file2)


def move_or_rename(fname, source, destination):

    # check if source and destination are strings

    if is_string(source):
        source = create_path(source)

    if is_string(destination):
        destination = create_path(destination)

    source = source / fname
    destination = destination / fname

    if not destination.exists():
        source.replace(destination)


def move_files(source_folder, destination_folder, filetype):
    search_str = f'*{filetype}*'
    for file in source_folder.rglob(search_str):
        source_path = Path(file)
        destination_path = destination_folder / file.name
        source_path.rename(destination_path)


def move_all_txt(source_folder, destination_folder):
    if is_string(source_folder):
        source_folder = create_path(source_folder)

    if is_string(destination_folder):
        destination_folder = create_path(destination_folder)

    for file in source_folder.glob('*'):
        if is_file(file) and file.suffix == '.txt':
            move_or_rename(file.name, source_folder, destination_folder)
        else:
            continue


def move_all_file_types(ftype, files, destination):

    # Set the destination path
    destination = create_path(destination)


    # get files by passing helper function
    if is_helper(files):

        files = files['all_dir_sub_files']
        for file in files:

            # Define the old source and new source
            file_src = file.parent / file.namev
            file_dst = destination / file.name

            if not file_dst.exists() and file.suffix == ftype:
                move_or_rename(file.name, file_srce, file_dst)
