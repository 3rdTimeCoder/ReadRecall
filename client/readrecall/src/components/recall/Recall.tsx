import React, { type JSX } from "react";
import { RecallContainer } from "./Recall.styles";
import SearchBar from "./search-bar/SearchBar";
import { useReadRecall } from "../../lib/hooks/use-readrecall";


const Recall = (): JSX.Element => {
    const { recall } = useReadRecall();

    const onSearch = async (query: string): Promise<void> => {
        console.log('query:', query);
        const res = recall(query);
        console.log('res:', res);
    }

    return (
        <RecallContainer>
            <SearchBar onSearch={onSearch} />
        </RecallContainer>
    )
}

export default Recall;