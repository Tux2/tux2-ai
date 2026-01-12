import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(working_path, file_path))
        if os.path.commonpath((working_path, full_path)) != working_path:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
             return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
             return f'Error: "{file_path}" is not a Python file'
        command = ["python3", full_path]
        if args != None:
            command.extend(*args)
        completed_process = subprocess.run(command, cwd=working_path, capture_output=True, text=True, timeout=30)
        status = []
        if completed_process.returncode != 0:
             status.append(f"Process exited with code {completed_process.returncode}")
        if completed_process.stdout == None or completed_process.stderr == None:
             status.append("No output produced")
        else:
            status.append(f"STDOUT: {completed_process.stdout}")
            status.append(f"STDERR: {completed_process.stderr}")
        return " ".join(status)
    except Exception as e:
        return f"Error: executing Python file: {e}"