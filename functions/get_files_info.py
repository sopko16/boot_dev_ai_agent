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
        

        result = ""
        for filename in os.listdir(target_dir_path):

            full_path = os.path.join(target_dir_path, filename)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)

            result += f"{filename}: file_size={file_size}, is_dir={is_dir}\n"
            # if os.path.isfile(full_path):
        return result
        # return f'Success: "{directory}" is within the working directory'

    except Exception as e:
        return f"Error: {e}"

# if __name__ == "__main__":
    print()
    # print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    # print(get_files_info("calculator", "/bin"))
    # print(get_files_info("calculator", "../"))