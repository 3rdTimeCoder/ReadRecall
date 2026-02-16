import React, { type JSX } from "react";
import { RecallContainer } from "./Recall.styles";
import SearchBar from "./search-bar/SearchBar";


const Recall = (): JSX.Element => {

    return (
        <RecallContainer>
            <SearchBar onSearch={()=>{}} />
        </RecallContainer>
    )
}

export default Recall;