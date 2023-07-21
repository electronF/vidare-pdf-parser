
# Built-in modules
import os
from typing import Dict, List, Union

# Extracted modules
import pypdf

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
                ouput_dir_path(str): The folder where image will be saved.
            Returns:
                None
        '''
        self.file_path = file_path
        file_name, _ = os.path.splitext(os.path.basename(file_path))
        self.output_texts_path = os.path.join(output_dir_path, file_name, 'texts')
        self.output_images_path = os.path.join(output_dir_path, file_name, 'images')
        
        if not os.path.exists(self.output_texts_path):
            os.makedirs(self.output_texts_path)
        
        if not os.path.exists(self.output_images_path):
            os.makedirs(self.output_images_path)
        
    
    def get_content(self) -> List[Dict[str, Union[str, int, Dict[str, Union[str, int]]]]]:   
        '''
            This function parse the PDF and return the content of the documents like
            text and images descriptions. The extracted data are saved on the provided 
            output dir.
            
            Args:\n
            Returns:
                (List[Dict[str, str | int | Dict[str, Union[str, int]]]]): The content of the PDF. The
                list of pages and associated images decription.
        '''     
        
        content:List[str, Union[str, int, Dict]] = []
        with open(self.file_path, "rb") as pdf_file:
            read_pdf = pypdf.PdfReader(pdf_file)
            for page_itr in range(len(read_pdf.pages)):
                page = read_pdf.pages[page_itr]
                page_content = page.extract_text()
                
                page_name = f'page{page_itr}.txt'
                page_path = os.path.join(self.output_texts_path, page_name)
                content.append({
                    'page': page_itr,
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
