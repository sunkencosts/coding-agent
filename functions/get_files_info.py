import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        abspath = os.path.abspath(working_directory)
        full_path = os.path.join(abspath, directory)
        target_path = os.path.normpath(full_path)

        valid_target_dir = os.path.commonpath([abspath, target_path]) == abspath

        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_path) is False:
            return f'Error: "{directory}" is not a directory'
        
        # List all items in the target directory
        items = os.listdir(target_path)
        items.sort()
        
        # Build the formatted string
        result_lines = []
        for item in items:
            item_path = os.path.join(target_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            result_lines.append(f"  - {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(result_lines)
    
    except Exception as e:
        return f"Error: {str(e)}"
