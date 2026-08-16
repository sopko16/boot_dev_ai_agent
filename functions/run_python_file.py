import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": (
            "Executes a Python file inside the permitted working directory. "
            "Use this when the user asks to run, execute, or test a Python program. "
            "Do not use this to list files or inspect directory contents."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the Python file to execute, relative to the "
                        "working directory. Example: 'main.py' or 'pkg/calculator.py'."
                    ),
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": (
                        "Optional command-line arguments to pass to the Python file. "
                        "Example: ['3 + 5']."
                    ),
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        wd_abs_path =  os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_abs_path, file_path))

        valid_file_path = os.path.commonpath([wd_abs_path, target_file_path]) == wd_abs_path

        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'


        command = ["python", target_file_path]

        if args:
            command.extend(args)

        completed_process = subprocess.run(
            command,
            cwd = wd_abs_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = []

        if completed_process.returncode != 0:
            output.append(
                f"Process exited with code {completed_process.returncode}"
            )
        if not completed_process.stdout and not completed_process.stderr:
            output.append("No output produced")
        else:
            if completed_process.stdout:
                output.append(
                    f"STDOUT:\n{completed_process.stdout}"
                )

            if completed_process.stderr:
                output.append(
                    f"STDERR:\n{completed_process.stderr}"
                )
        
        return "\n".join(output)
                
    
    except Exception as e:
        return f"Error: executing Python file: {e}"