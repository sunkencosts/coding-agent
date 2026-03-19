import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the file content of a specified file and returns the content as a string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path of the file to retrieve the contents of. relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
def get_file_content(working_directory, file_path):
    try:
        abspath = os.path.abspath(working_directory)
        full_path = os.path.join(abspath, file_path)
        target_path = os.path.normpath(full_path)

        valid_target_dir = os.path.commonpath([abspath, target_path]) == abspath

        if valid_target_dir is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_path) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"' 

        MAX_CHARS = 10000

        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            truncated = len(f.read(1)) > 0
        
        content = file_content_string

        if truncated:
            content += f'[...File "{target_path}" truncated at {MAX_CHARS} characters]'
        
        return content
    except Exception as e :
        return (f"Error: could not get file content{e}")
