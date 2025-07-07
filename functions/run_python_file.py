import os
import subprocess
from google.genai import types

from config import TIMEOUT
def run_python_file(working_directory, file_path, args=None):
    working_directory = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not os.path.isfile(file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        commands = ["python", file_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            timeout=TIMEOUT,
            capture_output=True,
            text=True,
            cwd=working_directory
        )
        output_parts = []
        if result.stdout.strip():
            output_parts.append("STDOUT:\n" + result.stdout.strip())
        if result.stderr.strip():
            output_parts.append("STDERR:\n" + result.stderr.strip())
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        return "\n".join(output_parts) if output_parts else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
