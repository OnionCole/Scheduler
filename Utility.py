"""
Written by Cole Anderson
"""
__author__ = "Cole Anderson"



# TXT FILE OPERATIONS
def output_list_to_txt(output: list, output_file_absolute_path: str, overwrite: bool):
    """
    Output a list of strings to a .txt file. If the end of the absolute path is not '.txt', the '.txt' file extension is appended by the function.
    :param output: list of strings
    :param output_file_absolute_path:
    :param overwrite: True if we should overwrite any information in the file, False if we should just append this data
    :return:
    """
    if overwrite:
        txt_alteration_operation = 'w'
    else:
        txt_alteration_operation = 'a'

    if output_file_absolute_path[-4:] != ".txt":  # if the path does not end in ".txt"
        output_file_absolute_path += ".txt"  # put the ".txt" onto the end

    with open(output_file_absolute_path, txt_alteration_operation) as txt_file:  # write
        txt_file.writelines(output)


def read_in_txt_as_list(input_file_absolute_path: str) -> list:
    """
    Read in a .txt file to a list
    :param input_file_absolute_path:
    :return: [line_1, ...]
    """
    with open(input_file_absolute_path, 'r') as txt_file:
        return [line.strip('\n') for line in txt_file.readlines()]
