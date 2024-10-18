from django_markdown_converter.helpers.utility import ReadSourceFromFile
from django_markdown_converter.helpers.processors import process_input_content


def get_source(path):
    chunk = ReadSourceFromFile(path)
    return process_input_content(chunk)