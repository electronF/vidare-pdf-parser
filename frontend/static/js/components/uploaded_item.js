class UploadedItem
{
    constructor(title, file_path, short_content, file_type, datetime, image_path='image-icon.webp')
    {
        this.title = title 
        this.file_path = file_path  
        this.short_content = short_content 
        this.file_type = file_type
        this.datetime = datetime
        this.image_path = image_path
    }

    render()
    {
        return $(`
            <div class="uploaded-item" title="${this.title.substring(0, 250)}">
                <div class="cover-image">
                    <img src="${this.image_path}" alt="cover image">
                </div>
                <div class="content-description">
                    <span class="title">${this.title}</span>
                    <span class="file-path">${this.file_path}</span>
                    <div class="text-content">${this.short_content}</div>
                    <div class="footer">
                        <div class="info">
                            <span class="file-type">${this.file_type}</span>
                            <span class="divider">|</span>
                            <span class="datetime">${this.datetime}</span>
                        </div>
                        <div class="actions">
                            <button> 
                                <img  class="icon" src="/static/images/trash-icon.webp" />
                                <span>Delete</span>
                            </button>
                            <button>
                                <img class="icon" src="/static/images/eye-icon.webp" />
                                <span>View</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `)
    }
}