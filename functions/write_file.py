import os

from functions.common.prepare_workpath import prepare_workpath, PermittedWorkDirError


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
