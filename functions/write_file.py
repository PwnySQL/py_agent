import os

from google.genai import types

from functions.common.prepare_workpath import prepare_workpath, PermittedWorkDirError


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a file with the content provided where path to the file is given by file_path which is relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            # working_directory omitted intentionally
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to write content to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="New content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    try:
        curr_file = prepare_workpath(working_directory, file_path)
        if os.path.isdir(curr_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(curr_file), exist_ok=True)
        with open(curr_file, "w") as f:
            f.write(content)
        # Return feedback string for LLM to stay in the feedback loop
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except PermittedWorkDirError as err:
        return str(err)
    except Exception as err:
        return f"Error: write_file throws an exception: {repr(err)}"
