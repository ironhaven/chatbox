import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs)
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not (result.stdout or result.stderr):
            output += "No output produced" 
        else:
            output += f"STDERR:{result.stderr}\nSTDOUT:{result.stdout}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"

