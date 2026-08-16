import os 

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Writes text content to a file inside the permitted working directory. "
            "Creates the file if it does not exist and overwrites it if it already exists."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the file to write, relative to the working directory. "
                        "Example: 'main.py' or 'pkg/new_file.py'."
                    ),
                },
                "content": {
                    "type": "string",
                    "description": (
                        "The text content to write to the file."
                    ),
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        wd_abs_path =  os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_abs_path, file_path))

        valid_file_path = os.path.commonpath([wd_abs_path, target_file_path]) == wd_abs_path

        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # if not os.path.isfile(target_file_path):
        #     return f'Error: File not found or is not a regular file: "{file_path}"'

        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        # Make sure parent directories exist
        parent_directory = os.path.dirname(target_file_path)
        os.makedirs(parent_directory, exist_ok=True)

        # Write/overwrite the file
        with open(target_file_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" '
            f'({len(content)} characters written)'
        )
    
    except Exception as e:
        return f"Error: {e}"
