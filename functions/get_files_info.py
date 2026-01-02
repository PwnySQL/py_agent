import os


# Treat directory as relative path to the working_directory such that the LLM agent can open files
# and directory, however NOT outside the working_directory which is set by the user.
def get_files_info(working_directory, directory="."):
    try:
        cwd = os.path.abspath(working_directory)
        curr_dir = os.path.normpath(os.path.join(cwd, directory))
        common = os.path.commonpath((cwd, curr_dir))
        if common != cwd:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
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
    except Exception as err:
        return f"Error: get_files_info throws an exception: {repr(err)}"
