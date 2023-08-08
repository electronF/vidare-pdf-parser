from typing import Dict, List, Union
from dataclasses import dataclass

@dataclass
class DocumentDTO:
    name:str
    path:str
    type:str
    cover_image_path:str
    pages:List[Dict[str, Union[str, int, Dict[str, str]]]]