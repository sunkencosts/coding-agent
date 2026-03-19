import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes content to a file at a given path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path of the file to write content to. relative to the working directory (default is the working directory itself)",
            ),
             "content": types.Schema(
                type=types.Type.STRING,
                description="the content to write to the file",
            ),
        },
    ),
)
def write_file(working_directory, file_path, content):
    try:
        abspath = os.path.abspath(working_directory)
        full_path = os.path.join(abspath, file_path)
        target_path = os.path.normpath(full_path)

        valid_target_dir = os.path.commonpath([abspath, target_path]) == abspath

        if valid_target_dir is False:
            return f'Error: Cannot write to "{target_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{target_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{target_path}" ({len(content)} characters written)'   

    except:
        raise Exception("Error: could not write file")

