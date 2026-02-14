import React, { useRef, useState, type JSX } from "react";
import { Buttons, FileListContainer, FileListItem, Uploader } from "./FileUploader.styles";
import { Book } from "lucide-react";


interface FileUploaderProps {
    onUpload: (files: FileList) => any;
}

type DocMimeType = 'application/pdf' | 'application/epub+zip';
type UploadStatus = 'idle' | 'uploading' | 'success' | 'error';

interface UploadFile {
    filename: string;
    filesize: number;
    fileType: DocMimeType;
    fileStatus: UploadStatus;
}




const FileUploader = ({ onUpload }: FileUploaderProps): JSX.Element => {   
    const [files, setFiles] = useState<FileList | null>(null);
    const [uploading, setUploading] = useState(false);
    const inputRef = useRef<HTMLInputElement | null>(null);
    

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;

        if (!files) return;
        setFiles(files);
    }

    const handleUpload = (): void => {
        if (files) {
            setUploading(true);
            onUpload(files);
        }
    }

    const openFilePicker = () => {
        inputRef.current?.click();
    }
    
    return (
        <Uploader>
            <input 
                ref={inputRef}
                type="file" 
                accept=".pdf,.epub,application/pdf,application/epub+zip"
                multiple
                onChange={handleFileChange} 
                style={{ 
                    display: 'none',
                    pointerEvents: 'none'
                 }}
            />
            <Buttons>
                {!uploading && <button type="button" onClick={openFilePicker}>Choose files</button>}
                {files && !uploading && (
                    <button onClick={handleUpload}>Upload</button>
                )}
            </Buttons>

            {files && (
                <FileListContainer>
                    {Array.from(files).map((file, index) => (
                         <FileListItem>
                            <span>{file.name}</span>
                            <span>{(file.size / (1024 * 1024)).toFixed(2)} MB</span>
                            {/* <span>{file.type}</span> */}
                        </FileListItem>
                    ))}
                </FileListContainer>
            )}

            {/* {files && !uploading && (
                <button onClick={handleUpload}>Upload</button>
            )} */}

        </Uploader>
    )

}


export default FileUploader;