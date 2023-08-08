
# Built-in modules
import os
from typing import Dict, List, Union

# External modules
from pdf2image import convert_from_path

#Local modules 
 
 
class PDF2ImageConverter:
    '''
        Convert PDF to Image
    '''
    
    def __init__(self, file_path:str, output_dir_path:str) -> None:
        '''
            PDF to image converter constructor.
            
            Args:
                file_path(str): The path of the PDF. 
                ouput_dir_path(str): The folder where image will be saved.
            Returns:
                None
        '''
        self.file_name, _ = os.path.splitext(os.path.basename(file_path))
        self.path_to_folder = os.path.join(output_dir_path)
        self.pdf_images = convert_from_path(file_path)
        
        if not os.path.exists(self.path_to_folder):
            os.makedirs(self.path_to_folder)
    
    def convert_first_page(self) -> str:
        '''
            Convert only the first page of the pdf as image and return the path of the image.
            Args:
            Returns:
                (str): The name of the first page on the disk as image. Or raise an error.
        '''
        file_path = '{}.png'.format(self.file_name)
        full_path = os.path.join(self.path_to_folder, file_path)
        self.pdf_images[0].save(
            fp=full_path,
            bitmap_format='png'
        )
        return file_path
        
    
    def convert_pages(self) -> List[str]:
        '''
            Save each page of the pdf as image on disk and return paths of files.
            
            Args:
            Returns:
                (List[str]): The list of names of pages of the pdf as images.
        '''
        #Create a directory with the name of the document on server to save images
        self.path_to_folder = os.path.join(self.path_to_folder, self.file_name)
        if not os.path.exists(self.path_to_folder):
            os.makedirs(self.path_to_folder)
        
        paths = []
        for index, image in enumerate(self.pdf_images):
            path = 'page{}.png'.format(index)
            image.save(
                fp=path,
                bitmap_format='png'
            )
            paths.append(path)
        return paths