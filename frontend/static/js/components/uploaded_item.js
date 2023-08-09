class UploadedItem {
  constructor(
    title,
    filePath,
    shortContent,
    fileType,
    dateTime,
    imagePath = "image-icon.webp"
  ) {
    this.title = title;
    this.filePath = filePath;
    this.shortContent = (shortContent??'').substring(0, 250);
    this.fileType = fileType;
    this.dateTime = (new Date(dateTime)).toUTCString();
    this.imagePath =
      typeof imagePath === "string" && imagePath.trim().length > 0
        ? imagePath
        : "image-icon.webp";
  }

  render() {
    return $(`
            <div class="uploaded-item" title="${this.title.substring(0, 250)}">
                <div class="cover-image">
                    <img src="/static/covers/${this.imagePath}" class="${(this.imagePath!="image-icon.webp")?'full-cover':''}" alt="cover image">
                </div>
                <div class="content-description">
                    <span class="title">${this.title}</span>
                    <span class="file-path">${this.filePath}</span>
                    <div class="text-content">${this.shortContent}</div>
                    <div class="footer">
                        <div class="info">
                            <span class="file-type">${this.fileType}</span>
                            <span class="divider">|</span>
                            <span class="datetime">${this.dateTime}</span>
                        </div>
                        <div class="actions">
                            <button class='delete'> 
                                <img  class="icon" src="/static/images/trash-icon.webp" />
                                <span>Delete</span>
                            </button>
                            <button class='preview'>
                                <img class="icon" src="/static/images/eye-icon.webp" />
                                <span>View</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `);
  }
}

export default UploadedItem;
