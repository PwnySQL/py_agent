import os
import subprocess

from functions.common.prepare_workpath import prepare_workpath, PermittedWorkDirError


def run_python_file(working_directory, file_path, args=None):
    try:
        curr_file = prepare_workpath(working_directory, file_path)
        if not os.path.isfile(curr_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        filename, file_extension = os.path.splitext(curr_file)
        if file_extension != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", curr_file]
        if args is not None:
            command.extend(args)

        completed_process = subprocess.run(
            command, cwd=working_directory, capture_output=True, text=True, timeout=30
        )

        ret = f"Process exited with code {completed_process.returncode}\n"
        if not completed_process.stderr and not completed_process.stdout:
            ret += "No output produced\n"
        else:
            if completed_process.stderr:
                ret += f"STDERR: {completed_process.stderr}\n"
            if completed_process.stdout:
                ret += f"STDOUT: {completed_process.stdout}\n"
        return ret

    except subprocess.TimeoutExpired:
        return f"Error: Running the python script {file_path} took longer than the time limit of 30s"
    except PermittedWorkDirError as err:
        return str(err)
    except Exception as err:
        return f"Error: executing Python file: {err}"
