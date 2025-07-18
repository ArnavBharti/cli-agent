import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not file_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        with open(file_path) as file:
            content = file.read(MAX_CHARS)
            if file.seek(0, os.SEEK_END) > MAX_CHARS:
                content = f"{content[:MAX_CHARS]}[...File \"{file_path}\" truncated at 10000 characters]."
            return content
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
