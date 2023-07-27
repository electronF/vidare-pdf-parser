import base64


class EncoderDecoder:
    '''
        Encode en Decode given texts.
    '''
    
    @classmethod
    def encode(cls, text:str)->str:
        '''
            Encode a given text.
            
            Args:
                text(str): The text to encode.
            Returns:
                (str): The encoded text
        '''
        text_bytes = text.encode('utf8')
        base64_bytes = base64.b64encode(text_bytes)
        return base64_bytes.decode('utf8')
        
    
    def decode(cls, text:str) -> str:
        '''
            Decode a given text.
            
            Args:
                text(str): The text to decode. It must had been obtained by this class encode method.
            Returns:
                (str): The decoded text.
        '''
        base64_bytes = text.encode('utf8')
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('utf8')
        