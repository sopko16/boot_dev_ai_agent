import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        wd_abs_path =  os.path.abspath(working_directory)
        target_dir_path = os.path.normpath(os.path.join(wd_abs_path, directory))

        valid_target_dir = os.path.commonpath([wd_abs_path, target_dir_path]) == wd_abs_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir_path):
            return f'Error: "{directory}" is not a directory'
        
        return f'Success: "{directory}" is within the working directory'
        
    except Exception as e:
        return f"Error: {e}"