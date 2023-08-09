#built-in modules
import os
import shutil
import glob
from typing import Union


class FileRemover:
    '''
        This class remove file from disc
    '''
    
    @classmethod
    def remove_file(cls, file_path:str) -> Union[str, None]:
        '''
            Remove the given file on the disc and return None if everything was well
            or None if not.
            
            Args:
                file_path(str): The file to the path to remove.
            Returns:
                (str | None): None if everything has been done well or
                    str if describing the error that occured.
        '''
        try:
            os.remove(file_path)
        except Exception as error:
            return str(error)
    
    @classmethod
    def remove_folder(cls, folder_path:str) -> Union[str, None]:
        '''
            Remove the given folder on the disc and return None if everything was well
            or None if not.
            
            Args:
                file_path(str): The folder to the path to remove.
            Returns:
                (str | None): None if everything has been done well or
                    str if describing the error that occured.
        '''
        try:
            shutil.rmtree(folder_path)
        except Exception as error:
            return str(error)
    
    @classmethod
    def remove_file_and_folder(cls, path:str, name:str) -> Union[str, None]:
        '''
            Remove the given files and folder with the given name on the
            given folder.
            
            Args:
                path(str): The path where to delete.
                name(str): The name of the file and folder to delete.
            Returns:
                (str | None): None if everything has been done well or
                    str if describing the error that occured.
        '''
        found = False
        for file_path in glob.glob(os.path.join(path, '*')):
            filename, _ = os.path.splitext(os.path.basename(file_path))
            if filename.lower().strip() == name.lower().strip():
                found = True
                try:
                    os.remove(file_path)
                except:
                    shutil.rmtree(file_path)
        if found == False:
            return f'No such directory named {path} or file named {name}'

    @classmethod
    def remove_all(cls, path:str) -> Union[str, None]:
        '''
            Remove files and folders in the given path.
            
            Args:
                path(str): The path where to delete everything.
            Returns:
                (str | None): None if everything has been done well or
                    str if describing the error that occured.
        '''
        if os.path.exists(path):
            for element_path in set(glob.glob(os.path.join(path, '*')) + glob.glob(os.path.join(path, '*.*'))):
                try:
                    os.remove(element_path)
                except Exception as error:
                    shutil.rmtree(element_path)              
        else:
            return 'No such file or directory name {}'.format(path)
