import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file, up to the first 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file including the filename you want to read, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(working_path, file_path))
        if os.path.commonpath((working_path, full_path)) != working_path:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
             return f'Error: File not found or is not a regular file: "{file_path}"'
        

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"