import os

from functions.common.prepare_workpath import prepare_workpath, PermittedWorkDirError


MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    try:
        curr_file = prepare_workpath(working_directory, file_path)
        if not os.path.isfile(curr_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(curr_file, "r") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return content
    except PermittedWorkDirError as err:
        return str(err)
    except Exception as err:
        return f"Error: get_files_content throws an exception: {repr(err)}"
