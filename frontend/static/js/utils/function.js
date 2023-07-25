function fileVerificator(file)
{
    if(file.size > 5 * 1024 * 1024)
    {
        return `The ${file.name} file has a size of ${fileSize(file)}. The maximum authorized size is 5Mo`   
    }
    else if(!(
            file.type.startsWith('application/') 
            &&  [
                'pdf', 
                'vnd.oasis.opendocument.text', 
                'vnd.ms-powerpoint', 
                'vnd.openxmlformats-officedocument.presentationml.presentation'
            ].includes(file.type.split('/')[1])
        ))
    {
        return `The file you choose is not a PDF, ODT, PPT or PPTX`
    }
}


function fileName(name)
{
    var part = ''.split('/')
    return part[part.length - 1].split('.')[0]
}


function fileSize(size)
{
    if(size < 1024)
        return `${size} B`
    else if(size < 1024*1024)
        return `${size/1024} KB`
    else if(size < 1024*1042*1024)
        return `${size/(1024 * 1024)} MB`
    return `${size/(1024 * 1024 * 1024)} GB`
}


export {fileVerificator, fileName, fileSize}