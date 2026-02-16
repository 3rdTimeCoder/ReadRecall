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

    scrollbar-width: none;
    -ms-overflow-style: none;
    &::-webkit-scrollbar {
        display: none;
    }
`;

export const FileListItem = styled.li`
    display: flex;
    justify-content: space-between;
    color: #111;
    width: 100%;
    list-style-type: none;
    border-bottom: 1px solid #dcb482ae;
    color: #DCB482;
    font-size: 1.3rem;
    gap: 1rem;

    & span {
        background: #DCB482;
        background: #111;
        padding: 1rem 2rem;
    }

    @media (max-width: 1280px) {
        font-size: 1rem;
    }

    @media (max-width: 1024px) { 
        font-size: 1rem;
    }

    @media (max-width: 972px) {
        & > span {
            padding: 0.5rem;
        }
    }

    @media (max-width: 768px) {
        font-size: 0.8rem;
    }

    @media (max-width: 630px) {
        font-size: 0.73rem;
    }

    @media (max-width: 410px) { 
        flex-direction: column;
        gap: 0;

        & > span {
            padding: 0.25rem;
            margin: 0;
        }
    }
    
`;

export const Buttons = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;

    @media (max-width: 630px) {
        flex-direction: column;
    }
`;