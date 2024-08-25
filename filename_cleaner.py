#!/usr/bin/python3 """This is a shebang for linux OS. It tells the OS to use the python3 interpreter"""

# DESCRIPTION: This program will format the names of all files and directories within one directory.
#   1) Uppercase characters are converted to lowercase.
#   2) Removes leading and trailing whitespaces.
#   3) Replaces whitespaces between charters with an underscore.
#   4) Remove multiple whitespaces in a row.
# USAGE:
#   Do not call this program with python or python3.
#   [filename_cleaner.py]: Prepares name changes in the CWD and prompts user to view changes before applying.
#   [filename_cleaner.py -f]: Force, apply name changes in the CWD.
#   [filename_cleaner.py absolute/path/to/dir]: Prepares name changes in the at "absolute/path/to/dir" and prompts user to view changes before applying.
#   [filename_cleaner.py absolute/path/to/dir -f]:  Force, apply name changes at "absolute/path/to/dir".
# OS:
#    Tested on WindowsOS and WSL Ubuntu Linux distro.

import os, sys

class Directory:
    def __init__(self, path=os.getcwd()):
        """If param path is not provided default to cwd"""
        if os.path.isdir(path):
            self._path = path
        else:
            raise InvalidPathToDirectory
        self._dir_contents = os.listdir(self._path)
        self._dir_contents_to_change = []

    def get_path(self) -> str:
        return self._path

    def prep(self) -> tuple:
        """
        Each name with a formatting issue in the directory is added to self._dir_contents_to_change.
        :return: tuple : (file count to be changed, directory count to be changed)
        """
        file_count, dir_count = 0, 0
        for name in self._dir_contents:
            name_change = self._clean_name(name)
            if name_change != name:
                path_to_content = os.path.join(self._path, name)
                content_type = None
                if os.path.isfile(path_to_content):
                    content_type = "file"
                    file_count += 1
                elif os.path.isdir(path_to_content):
                    content_type = "dir"
                    dir_count += 1

                self._dir_contents_to_change.append((name, name_change, content_type))
        return file_count, dir_count

    def preview_changes(self) -> list:
        return self._dir_contents_to_change

    def apply_changes(self) -> tuple:
        """
        Content names in the self._path dir to are altered if they are present in self._dir_contents_to_change.
        Return tuple(count of files changed, count of dirs changed)
        """
        file_count, dir_count = 0, 0
        for content in self._dir_contents_to_change:
            name, new_name, file_or_dir = content
            if file_or_dir == "file":
                file_count += 1
            elif file_or_dir == "dir":
                    dir_count += 1
            cur_name = os.path.join(self._path, name)
            new_name = os.path.join(self._path, new_name)
            os.rename(cur_name, new_name)
        return file_count, dir_count

    def _clean_name(self, name: str) -> str:
        """
        Removes whitespaces from the beginning and ends of the file name.
        All alphabetic chars turned to lowercase.
        Whitespaces between chars are turned to underscores.
        Multiple whitespaces in a row are removed.
        Don't mess with extensions.
        """
        content_name_and_ext = os.path.splitext(name)                   # split extension from content name
        content_name = content_name_and_ext[0].strip()                  # remove leading/trailing whitespaces.

        i, out = 0, ""
        while i < len(content_name):
            if content_name[i].isupper():
                out += content_name[i].lower()
            elif content_name[i] == " ":
                if out[len(out) - 1] != "_":
                    out += "_"
            else:
                out += content_name[i]
            i += 1
        if len(content_name_and_ext) > 1:
            for ext in content_name_and_ext[1:]:                        # add extensions back
                out += ext
        return out

class InvalidPathToDirectory(Exception):
    def __init__(self):
        self._message = "The provided path is not a path to a directory."
    def __str__(self):
        return self._message

def print_preview_name_changes(name_changes: list) -> None:
    print(
        '    -----------------------------------\n    Current Name | Altered Name | Type:\n    -----------------------------------')
    for name in name_changes:
        print(f'    {name[0]} | {name[1]} | {name[2]}.')
    print()

def print_usage() -> None:
    prompt = f'File_name_cleaner.py USAGE:\ninvalid args: {args} expects at most 2 args.\ndefault: no args. Program prompts the number of files and directories in the cwd that it will rename.\n-f: force. Program renames files and dirs in the CWD. force can follow path to force rename at the directory specified in path.\n"total/path/to/dir": path. Program preforms default function at the specified path.\n'
    print(prompt)

if __name__ == "__main__":
    args = sys.argv
    args_len = len(args)
    if args_len == 1:                                                                                    # 1:default cwd
        dir = Directory()
        renameable = dir.prep()
        if renameable[0] == 0 and renameable[1] == 0:
            print(f'The file names within {dir.get_path()} are already formatted properly.')
            exit()
        else:
            print(f'There are {renameable[0]} file(s) and {renameable[1]} dir(s) that can be renamed in {dir.get_path()}.')

            loop, name_changes = True, None
            while loop:                                                                                  # view changes?
                user_input = input(f'Enter v to view changes before applying or q to quit: ')
                if user_input.lower() == 'q':
                    loop = False
                    exit()
                elif user_input.lower() == 'v':
                    loop = False
                    name_changes = dir.preview_changes()
                else:
                    print(f'Invalid option: {user_input} is not "v" or "q".')

            print_preview_name_changes(name_changes)

            loop, count_renamed = True, None                                                             # apply changes?
            while loop:
                user_input = input(f'Enter a to to apply changes or q to quit: ')
                if user_input.lower() == 'q':
                    loop = False
                    exit()
                elif user_input.lower() == 'a':
                    loop = False
                    count_renamed = dir.apply_changes()
                else:
                    print(f'Invalid option: {user_input} is not "v" or "q".')

                print(f'{count_renamed[0]} files were renamed and {count_renamed[1]} directories were renamed.')

    elif args_len == 2:

        if args[1] == '-f':                                                                                # 2:force cwd
            dir = Directory()
            renameable = dir.prep()
            if renameable[0] == 0 and renameable[1] == 0:
                print(f'The file names within {dir.get_path()} are already formatted properly.')
                exit()
            else:
                count_renamed = dir.apply_changes()
                print(f'{count_renamed[0]} files were renamed and {count_renamed[1]} directories were renamed.')

        elif os.path.isdir(args[1]):                                                                 # 3:default at path
            dir = Directory(args[1])
            renameable = dir.prep()
            if renameable[0] == 0 and renameable[1] == 0:
                print(f'The file names within {dir.get_path()} are already formatted properly.')
                exit()
            else:
                print(
                    f'There are {renameable[0]} file(s) and {renameable[1]} dir(s) that can be renamed in {dir.get_path()}.')
                loop, name_changes = True, None
                while loop:  # view changes?
                    user_input = input(f'Enter v to view changes before applying or q to quit: ')
                    if user_input.lower() == 'q':
                        loop = False
                        exit()
                    elif user_input.lower() == 'v':
                        loop = False
                        name_changes = dir.preview_changes()
                    else:
                        print(f'Invalid option: {user_input} is not "v" or "q".')

                print_preview_name_changes(name_changes)

                loop, count_renamed = True, None  # apply changes?
                while loop:
                    user_input = input(f'Enter a to to apply changes or q to quit: ')
                    if user_input.lower() == 'q':
                        loop = False
                        exit()
                    elif user_input.lower() == 'a':
                        loop = False
                        count_renamed = dir.apply_changes()
                    else:
                        print(f'Invalid option: {user_input} is not "v" or "q".')

                    print(f'{count_renamed[0]} files were renamed and {count_renamed[1]} directories were renamed.')

        else:                                                                                           # no valid input
            print_usage()

    elif args_len == 3:
        if os.path.isdir(args[1]) and args[2] == '-f':                                                 # 4:force at path
            dir = Directory(os.getcwd())
            renameable = dir.prep()
            if renameable[0] == 0 and renameable[1] == 0:
                print(f'The file names within {dir.get_path()} are already formatted properly.')
                exit()
            else:
                count_renamed = dir.apply_changes()
                print(f'{count_renamed[0]} files were renamed and {count_renamed[1]} directories were renamed.')
        else:                                                                                           # no valid input
            print_usage()
    else:                                                                                               # no valid input
        print_usage()