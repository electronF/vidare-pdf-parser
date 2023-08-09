import UploadingItem from "../components/uploading_item.js"
import saveFile from "../hooks/sendfile.js";
import { fileVerificator, fileSize, fileName } from "../utils/function.js";
import {POST_DOCUMENT} from "../constants.js";
import UploadedSection from "./uploaded_section.js";


class UploadingSection
{
    constructor()
    {
        this.uploadedSection = new UploadedSection()
    }

    async uploadFile(file, path, uploadingItem)
    {
        var response = await saveFile(file, path, POST_DOCUMENT)
        if (response['success'] === false)
        {
            alert(response['message'])
        }
        else
        {
            uploadingItem.remove()  
            this.uploadedSection.addItem(response)    
        }
    }

    #evenListenner(){
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
            
            inputFiles[0].onchange = ()=> {
                var count = 0
                var files = {}
                var paths = inputFiles[0].value.split(';')
                for(var file of inputFiles[0].files)
                {
                    var message = fileVerificator(file)
                    if(message===null)
                    {
                        count++; 
                        var uploadingItem = $(
                            (new UploadingItem(
                                count, 
                                fileName(file.name), 
                                `${fileSize(file.size)}`, 
                                file.type.split('/')[1])
                            ).render()
                        )
                        uploadedItems.append(uploadingItem)
                        files[`file-${count}`] = {'file':file, 'path': paths[count-1]}
                        this.uploadFile(file, paths[count-1], uploadingItem)
                    } 
                    else
                    {
                        alert(message)
                    }   
                }
            }
        })
    }

    listen ()
    {
        this.#evenListenner()
    }
}


export default UploadingSection