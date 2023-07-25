import UploadingItem from "./components/uploading_item.js"

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
        
        for(var file of inputFiles[0].files)
        {

            count++; 
            uploadedItems.append(
                (new UploadingItem(
                    count, 
                    file.name, 
                    `${(file.size/(1024 * 1024)).toFixed(2)} Mo`, 
                    file.type.split('/')[1])
                ).render()
            )
            files[`file-${count}`] = file
        }
    }
})
