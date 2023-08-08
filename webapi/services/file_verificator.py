import os

ALLOWED_FILE_TYPES = ['odt', 'pdf', 'ppt', 'pptx']


class FileVerificator:
    '''
        This class is use to verify file information as file type, size
    '''
    
    @classmethod
    def is_file_in_allowed_type(cls, file_path:str) -> (bool):
        '''
            Check if the file is in the right type ie: ODT, PDF, PPT, PPTX.
            
            Args: 
                file_path(str): The path to the file
            Returns:
                (bool): True if the file is in the right type or False if not.
        '''
        _, ext = os.path.splitext(os.path.basename(file_path))
        if ext.lower()[1:] in ALLOWED_FILE_TYPES:
            return True
        return False
    
    @classmethod
    def is_good_allowed_type(cls, file_type:str)-> (bool):
        '''
            Check if the file type is an allowed type ie: ODT, PDF, PPT, PPTX.
            
            Args:
                file_type(str): The type to check if it is an allowed type.
            Returns:
                (bool): The if the type is in allowed type or flase if not
        '''
        return file_type.lower() in ALLOWED_FILE_TYPES 
    
    @classmethod
    def get_type(cls, file_path:str) -> (str):
        '''
            Get the type of a file.
            
            Args:
                file_path(str): The path to the file.
            Returns:
                (str): The type of the file.
        '''
        return os.path.splitext(os.path.basename(file_path))[1].upper()[1:]
    
    @classmethod
    def file_size(cls, file_path) -> (int):
        '''
            Get the size of the file in bytes.
            
            Args:
                file_path(str): The path to the file.
            Returns:
                (int): The size of the file in bytes.
        '''
        return os.path.getsize(file_path)
    
    @classmethod
    def is_the_size_good(cls, file_path:str, limit=5*1024*1024) -> (bool):
        '''
            Get if the file size do not exced limit.
            
            Args:
                file_path(str): The path to the file.
                limit(int): The maximal size of the file in bytes.
            Returns:
                (bool): True if the size of the file is good and False if not.
        '''
        return os.path.getsize(file_path) <= limit  