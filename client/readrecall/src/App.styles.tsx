import styled from "styled-components";
import bookVector from '../public/book-vector-1.png';
import BooksBackground from '../public/assets/books2.png';
// import BooksBackground from '../public/assets/imsgr.png';


export const AppContainer = styled.div`
    width: 100vw;
    height: 100vh;
    position: relative;
    padding: 5rem 2rem;

    display: flex;
    flex-direction: column;
    align-items: center;
    /* background: linear-gradient(
        to right,
        #251231,
        #2b4948
    ); */
    background: linear-gradient(
        90deg,
        #361d50 0%,
        #2c1d47 35%,
        #191d39 70%,
        #080e26 100%
    );

    background: linear-gradient(180deg, #252427 0.000%, #2c2833 20.000%, #3b334e 40.000%, #51426a 60.000%, #6f5879 80.000%, #947373 100.000%);
    background: #606C5A;;

    & h1 {
        /* margin-top: -5rem; */
        /* margin-left: 3rem; */
        /* color: #606C5A; */
        margin-top: 2rem;
        font-size: 4rem;
        background: #0a090993;
        z-index: 300;

       box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);
        -webkit-box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);
        -moz-box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);
    }

`;

export const BookVector = styled.div`
    width: 400px;
    height: 400px;
    background: url(${bookVector});
    background-size: contain;
    background-repeat: no-repeat;
    /* border: 1px solid blue; */
    margin-left: -5rem;

    /* position: absolute;
    bottom: -60px;
    left: -50px; */
`;

export const BookVectorContainer = styled.div`
    width: 250px;
    height: 230px;
    background-color: #0a090950;
    border-radius: 50%;
    display: grid;
    place-content: center;

    box-shadow: 10px 2px 81px -15px rgba(0,0,0,0.55) inset;
    -webkit-box-shadow: 10px 2px 81px -15px rgba(0,0,0,0.55) inset;
    -moz-box-shadow: 10px 2px 81px -15px rgba(0,0,0,0.55) inset;

    box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.43) inset;
    -webkit-box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.43) inset;
    -moz-box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.43) inset;
`;


export const BookBackground = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100%;
    background: url(${BooksBackground});
    background-size: cover;
    background-repeat: no-repeat;
    opacity: 0.5;
`;
