import { useCallback } from "react";
import { uploadFiles } from "../../api/upload-files";
import { recallBook } from "../../api/recall-book";


interface ReadRecallReturn {
    upload: (files: FileList) => Promise<void>;
    recall: (query: string) => Promise<void>;
}

const useReadRecall = (): ReadRecallReturn => {

    // TDOD
    const upload = useCallback(async (files: FileList) => {
        const res = await uploadFiles(files);
        console.log(res);
    }, []);


    const recall = useCallback(async (query: string) => {
        const res = recallBook(query);
        console.log(res);
    },[]);


    return { upload, recall }
}

export { useReadRecall };