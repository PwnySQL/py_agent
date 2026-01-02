import os

from functions.common.prepare_workpath import prepare_workpath, PermittedWorkDirError


# Treat directory as relative path to the working_directory such that the LLM agent can open files
# and directory, however NOT outside the working_directory which is set by the user.
def get_files_info(working_directory, directory="."):
    try:
        curr_dir = prepare_workpath(working_directory, directory)
        if not os.path.isdir(curr_dir):
            return f'Error: "{directory}" is not a directory'
        readable_name = directory
        if readable_name == ".":
            readable_name = "current"
        ret = [f"Result of {readable_name} directory"]
        for itm in os.listdir(curr_dir):
            path = os.path.join(curr_dir, itm)
            is_dir = os.path.isdir(path)
            size = os.path.getsize(path)
            ret.append(f"  - {itm}, file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(ret)
    except PermittedWorkDirError as err:
        return str(err)
    except Exception as err:
        return f"Error: get_files_info throws an exception: {repr(err)}"
