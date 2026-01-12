import os

def get_files_info(working_directory, directory="."):
    try:
        working_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(working_path, directory))
        if os.path.commonpath((working_path, full_path)) != working_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        file_strings = []
        files = os.listdir(full_path)
        for file in files:
            file_path = os.path.join(full_path, file)
            file_size = os.path.getsize(file_path)
            file_is_dir = os.path.isdir(file_path)
            file_strings.append(f" - {file}: file_size={file_size} bytes, is_dir={file_is_dir}")
        full_string = "\n".join(file_strings)
        return full_string
    except Exception as e:
        return f"ERROR: {e}"