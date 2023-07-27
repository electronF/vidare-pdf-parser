# built-in
import os
import uuid

from typing import Union

# third party module
from werkzeug.datastructures import FileStorage

#Local module
from webapi.services.encoder_decoder import EncoderDecoder

#Constants
DIVIDER = '---&&---'



def safe_filename(filename:str):
    '''
        Create a safe file to prevent injection.
        
        Args: 
            filename(str): The filename to make safety.
        Returns:
            (str): The safe file name.
    '''
    name, extension = os.path.splitext(os.path.basename(filename))
    return f'{EncoderDecoder.encode(name)}{DIVIDER}{str(uuid.uuid1())}{extension}'
    

def save_file(file:FileStorage, output_path:str) -> Union[str, None]:
    '''
        Save a file to a given output directory.
        
        Args:
            file(FileStorage): The file to save.
            output_path(str): The full path to a directory where to save the file.
        Returns:
            (str | None): The save filename if the file where save successfully or None if not.
    '''
    filename = os.path.abspath(file.filename)
    for attempt_nbr in range(10):
        safe_name = safe_filename(filename)
        output_file_path = os.path.join(os.path.join(output_path, safe_name))
        if not os.path.exists(output_file_path):
            file.save(output_file_path)
            return safe_name
    return None


def get_original_filename(filename:str) -> Union[str, None]:
    '''
        Return the original filename of a file. The given filename must have been obtained
        by the function `safe_filename` of this module.
        
        Args:
            filename(str): The encoded file name to get original name.
        Returns:
            (str | None): The original filename if it has been obtained successfully of None if not.
    '''
    formated_filename, _uuid = filename.split(DIVIDER)
    try:
        return EncoderDecoder.decode(formated_filename)
    except:
        return None
