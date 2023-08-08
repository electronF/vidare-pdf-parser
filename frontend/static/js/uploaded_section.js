import UploadedItem from "./components/uploaded_item.js";
import {GET_DOCUMENT} from "./constants.js";

class UploadedSection
{
    addItem(itemDescriptiom){
        console.log({itemDescriptiom})
        // Object.keys(itemDescriptiom).includes()
        var uploadedItem = $(
            (new UploadedItem(
                itemDescriptiom['name'],
                itemDescriptiom['name'],
                itemDescriptiom['content'],
                'pdf',
                (new Date()).toISOString(),
                itemDescriptiom['cover_image_path']
            )).render()
        )

        var uploadedItems = $('#uploaded-files')
        uploadedItems.append(uploadedItem)
    }
}

export default UploadedSection