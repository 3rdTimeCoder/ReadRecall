import styled from "styled-components";
import bookVector from './assets/book-vector-1.png';
import BooksBackground from './assets/books2.png';
// import BooksBackground from '../public/assets/imsgr.png';


export const AppContainer = styled.div`
    width: 100vw;
    height: 100vh;
    position: relative;
    padding: 5rem 2rem;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
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
    background: #606C5A;
    background: #111;

    box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.43) inset;
    -webkit-box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.43) inset;
    -moz-box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.43) inset;

`;

export const Logo = styled.div`
        /* margin-top: -5rem; */
        /* margin-left: 3rem; */
        /* color: #606C5A; */
        /* margin-top: 2rem; */
        font-size: 1.5rem;
        background: #0a090993;
        z-index: 300;
        padding: 1rem;
        position: absolute;
        top: 0;
        left: 0;
        border-bottom: 1px solid #DCB482;

        & h1 {
            margin-bottom: 0;
        }

       box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);
        -webkit-box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);
        -moz-box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);

    /* Desktop and down */
    @media (max-width: 1280px) {
        font-size: 1rem;
    }

    /* Laptop and down */
    @media (max-width: 1024px) { 
        /* font-size: 1rem; */
    }

    /* Tablet and down */
    @media (max-width: 768px) {
        /* font-size: 1rem; */
    }

    /* Mini-Tablet and down */
    @media (max-width: 630px) {
        font-size: 0.73rem;
    }
    
    


    

`;

export const BookVector = styled.div`
    width: 700px;
    height: 600px;
    background: url(${bookVector});
    background-size: contain;
    background-repeat: no-repeat;
    /* border: 1px solid blue; */
    margin-left: -5rem;

    /* position: absolute;
    bottom: -60px;
    left: -50px; */

     @media (max-width: 1280px) {
        width: 460px;
        height: 470px;
    }

    @media (max-width: 1024px) { 
        width: 360px;
        height: 330px;
    }

    @media (max-width: 630px) {
        width: 400px;
        height: 350px;
    }
`;

export const BookVectorContainer = styled.div`
    width: 390px;
    height: 370px;
    /* background-color: #0a090950; */
    background-color: #DCB482;
    border-radius: 50%;
    display: grid;
    place-content: center;
    margin-bottom: 4rem;


    box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.73) inset;
    -webkit-box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.73) inset;
    -moz-box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.73) inset;

    @media (max-width: 1280px) {
        width: 270px;
        height: 250px;
    }

    @media (max-width: 1024px) { 
        width: 230px;
        height: 210px;
        margin-bottom: 2rem;
    }

    @media (max-width: 630px) {
        width: 270px;
        height: 250px;
    }
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


export const MainLayout = styled.div`
    /* display: flex;
    justify-content: space-around;
    align-items: center; */
`;