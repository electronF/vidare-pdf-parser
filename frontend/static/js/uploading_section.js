import UploadingItem from "./components/uploading_item.js"
import { fileVerificator, fileSize, fileName } from "./utils/function.js";

$('div.upload-section .browse-button').on('click', ()=>{
    var uploadedItems = $('#uploading-items');
    var inputFiles = $(`<input 
        type='file' 
        accept='
            application/pdf, 
            application/vnd.oasis.opendocument.text, 
            application/vnd.ms-powerpoint, 
            application/vnd.openxmlformats-officedocument.presentationml.presentation
            ' 
        multiple 
    />`)
    inputFiles.click()
    
    inputFiles[0].onchange = () => {
        var count = 0
        var files = {}
        var paths = inputFiles.value.split(';')
        
        for(var file of inputFiles[0].files)
        {
            var message = fileVerificator(file)
            if(message===null)
            {
                count++; 
                
                uploadedItems.append(
                    (new UploadingItem(
                        count, 
                        fileName(file.name), 
                        `${fileSize(file.size)}`, 
                        file.type.split('/')[1])
                    ).render()
                )
                files[`file-${count}`] = {'file':file, 'path': paths[count-1]}
            } 
            else
            {
                alert(message)
            }   
        }
    }
})
