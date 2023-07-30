
# Built-in modules
import os
import uuid
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
        file_name, _ = os.path.splitext(os.path.basename(file_path))
        self.path_to_folder = os.path.join(output_dir_path, file_name)
        self.pdf_images = convert_from_path(file_path)
        
        if not os.path.exists(self.path_to_folder):
            os.makedirs(self.path_to_folder)
    
    def convert_first_page(self) -> str:
        '''
            Convert only the first page of the pdf as image and return the path of the image.
            Args:
            Returns:
                (str): The path of the first page on the disk as image. Or raise an error.
        '''
        path = os.path.join(self.path_to_folder, 'page0-{}.png'.format(str(uuid.uuid1())))
        self.pdf_images[0].save(
            fp=path,
            bitmap_format='png'
        )
        return path
        
    
    def convert_pages(self) -> List[str]:
        '''
            Save each page of the pdf as image on disk and return paths of files.
            
            Args:
            Returns:
                (List[str]): The list of paths of pages of the pdf as images.
        '''
        
        paths = []
        for index, image in enumerate(self.pdf_images):
            path = os.path.join(self.path_to_folder, 'page{}.png'.format(index))
            image.save(
                fp=path,
                bitmap_format='png'
            )
            paths.append(path)
        return paths