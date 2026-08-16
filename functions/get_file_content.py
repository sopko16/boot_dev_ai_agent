import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": (
            "Reads and returns the text contents of a file inside the permitted "
            "working directory. Use this when the user asks to inspect, read, "
            "or view a specific file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the file to read, relative to the working directory. "
                        "Example: 'main.py' or 'pkg/calculator.py'."
                    ),
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        wd_abs_path =  os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_abs_path, file_path))

        valid_file_path = os.path.commonpath([wd_abs_path, target_file_path]) == wd_abs_path

        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'


        with open(target_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    
        return file_content_string

    except Exception as e:
        return f"Error: {e}"