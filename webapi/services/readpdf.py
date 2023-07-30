# Built-in modules
import os
from typing import Dict, List, Union

# Extracted modules
import PyPDF2 as pypdf

#Local modules


class PdfParser:
    '''
        Parse PDF file.
    '''
    
    def __init__(self, file_path:str, output_dir_path:str) -> None:
        '''
            PDF parser constructor.
            
            Args:
                file_path(str): The path of the PDF. 
                ouput_dir_path(str): The folder where texts and images will be saved.
            Returns:
                None
        '''
        self.file_path = file_path
        file_name, _ = os.path.splitext(os.path.basename(file_path))
        self.path_to_folder = os.path.join(output_dir_path, file_name)
        self.output_texts_path = os.path.join(self.path_to_folder, 'texts')
        self.output_images_path = os.path.join(self.path_to_folder, 'images')
        
        if not os.path.exists(self.output_texts_path):
            os.makedirs(self.output_texts_path)
        
        if not os.path.exists(self.output_images_path):
            os.makedirs(self.output_images_path)
        
    
    def get_content(self) -> List[Dict[str, Union[str, int, Dict[str, str]]]]:   
        '''
            This function parse the PDF and return the content of the documents like
            text and images descriptions. The extracted data are saved on the provided 
            output dir.
            
            Args:\n
            Returns:
                (List[Dict[str, str | int | Dict[str, str]]]): The content of the PDF. The
                list of pages and associated images decription.
        '''     
        
        content:List[Dict[str, Union[str, int, Dict[str, str]]]] = []
        with open(self.file_path, "rb") as pdf_file:
            pdf_reader = pypdf.PdfReader(pdf_file)
            for page_itr in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_itr]
                page_content = page.extract_text()
                
                page_name = f'page{page_itr}.txt'
                page_path = os.path.join(self.output_texts_path, page_name)
                content.append({
                    'number': page_itr,
                    'text': page_content,
                    'path': page_path,
                    'images': []
                })
                
                with open(page_path, 'w', encoding='utf8') as out_page:
                    out_page.write(page_content)
                
                for index, image in enumerate(page.images):
                    image_path = os.path.join(self.output_images_path, image.name)
                    with open(image_path, "wb") as fp:
                        fp.write(image.data)
                        content[-1]['images'].append(
                            {
                                'name': image.name,
                                'order': index,
                                'path': image_path 
                            }
                        )
    
        return content 
    
    def split_first_page(self)->str:
        '''
            This method split the first page of the PDF and return a path to this page
            on the disk.
            
            Args:
            Returns:
                (str): The path to the page on the disk or raise an error.
        '''
        with open(self.file_path, "rb") as pdf_file:
            pdf_reader = pypdf.PdfReader(pdf_file)
            pdf_writer = pypdf.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[0])
            output_filename = os.path.join(self.path_to_folder, 'page0.pdf')
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)
            return output_filename