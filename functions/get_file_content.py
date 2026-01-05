import os

from google.genai import types

from functions.common.prepare_workpath import prepare_workpath, PermittedWorkDirError


MAX_CHARS = 10000


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Read file content given a specific path to a file relative to the working directory. Output is limited to {MAX_CHARS} characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            # working_directory omitted intentionally
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to read content form, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)


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
