class UploadingItem
{
    constructor(id, name, size, type='PDF' )
    {
        this.id = id
        this.name = name
        this.type = type
        this.size = size
    }

    render(){
        return $(`
            <div class="uploading-items" id="${this.id}">
                <div class="uploading-item">
                    <div class="logo">
                        <img src="/static/images/${((this.type.toLocaleUpperCase() != 'PDF')?'PPT Doc.webp':'PDF Doc.webp')}" />   
                    </div>
                    <div class="details">
                        <div class="header">
                            <span class="name">${this.name}</span>
                            <span class="size">${this.size}</span>
                            <button class="close">
                                <img src="/static/images/close-icon.webp" alt="close">
                            </button>
                        </div>
                        <div class="progress-bar">
                            <input type="range" min="0" max="100" id="progress-${this.id}" disabled>
                        </div>
                        <div class="progression-label">
                            <span class="percentage" id="percentage-${this.id}">0%</span>
                            <span>done</span>
                        </div>
                    </div>
                </div>
            </div>
        `)
    }
}

export default UploadingItem