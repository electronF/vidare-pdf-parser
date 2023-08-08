import UploadedItem from "../components/uploaded_item.js";

class UploadedSection
{
    uploadedItems = $('#uploaded-files')
    addItem(itemDescriptiom){
        var uploadedItem = $(
            (new UploadedItem(
                itemDescriptiom['title']??'',
                itemDescriptiom['path'],
                itemDescriptiom['short_content'],
                itemDescriptiom['type'],
                itemDescriptiom['add_at'],//(new Date()).toISOString()
                itemDescriptiom['cover_image_path']
            )).render()
        )
       this.uploadedItems.append(uploadedItem)
    }

    clear(){
        this.uploadedItems.empty()
    }
}

export default UploadedSection