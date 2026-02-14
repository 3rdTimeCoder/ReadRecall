import styled from "styled-components";


export const Uploader = styled.div`
    display: grid;
    place-items: center;
    width: 90%;
    max-width: 850px;
    pointer-events: all;
    cursor: pointer;
    z-index: 100;
    & > * {
        z-index: 100;
    }
`;

export const FileListContainer = styled.ul`
    background: transparent;
    border-radius: 20px;

    width: 100%;
    height: 100%;
    max-height: 35vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 0%;
    font-size: 1.1rem;

    /* background-color: #DCB482; */

    /* box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);
    -webkit-box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);
    -moz-box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32); */

    /* border: 1px solid red; */
    scrollbar-width: none;
  /* IE and Edge */
    -ms-overflow-style: none;
    &::-webkit-scrollbar {
        display: none;
    }
`;

export const FileListItem = styled.li`
    display: flex;
    /* flex-direction: column; */
    justify-content: space-between
    ;
    /* padding: 1rem 2rem; */
    /* border-bottom: 1px solid #111; */
    color: #111;
    width: 100%;
    list-style-type: none;
    border-bottom: 1px solid #dcb482ae;
    color: #DCB482;
    font-size: 1.3rem;
    

    & span {
        background: #DCB482;
        background: #111;
        padding: 1rem 2rem;
    }


    /* border: 1px solid blue; */
`;

export const Buttons = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
`;