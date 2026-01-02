import os


class PermittedWorkDirError(ValueError):
    pass


def prepare_workpath(working_directory, path):
    cwd = os.path.abspath(working_directory)
    abs_path_in_wd = os.path.normpath(os.path.join(cwd, path))
    common = os.path.commonpath((cwd, abs_path_in_wd))
    if common != cwd:
        raise PermittedWorkDirError(
            f'Error: Cannot list "{path}" as it is outside the permitted working directory'
        )
    return abs_path_in_wd
