import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file and returns the output from stdout or stderr",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path of the file to run. relative to the working directory (default is the working directory itself)",
            ),
             "args": types.Schema(
                type=types.Type.ARRAY,
                description="array of arguements to extend the python run command with",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
def run_python_file(working_directory, file_path, args=None):
    try:
        abspath = os.path.abspath(working_directory)
        full_path = os.path.join(abspath, file_path)
        target_path = os.path.normpath(full_path)

        valid_target_dir = os.path.commonpath([abspath, target_path]) == abspath

        if valid_target_dir is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_path) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_path.endswith('.py') is False:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if args:
            command.extend(args)
        
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        
        output = ''
        if result.returncode != 0:
            output = f"Process exited with code {result.returncode}"
        if result.stdout is None or result.stderr is None:
            output = "No output produced"
        
        if result.stdout:
            output = f"STDOUT: {result.stdout}"
        if result.stderr:
            output = f"STDERR: {result.stderr}"
        return output
        
    except Exception as e :
        raise Exception(f"Error: executing Python file: {e}")