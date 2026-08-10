import { createGlobalStyle } from 'styled-components';

export const GlobalStyle = createGlobalStyle`
  *, *::before, *::after {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: 'EB Garamond', serif;
    font-family: 'Merriweather';
    font-weight: 500;
    line-height: 1.6;
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: 'UnifrakturMaguntia', cursive;
    margin-top: 0;
    margin-bottom: 1rem;
    color: #DCB482;
  }

  p {
    /* font-family: 'Almendra Display', serif; */
    font-family: "UnifrakturMaguntia", cursive;
    font-weight: 400;
    font-style: normal;
    margin-top: 0;
    margin-bottom: 1rem;
    color: ${({ theme }) => theme.colors.darkGray};
  }

  button {
    font-family: 'Almendra Display', serif;
    color: #DCB482;
    border-radius: 40px;
    width: 350px;
    font-size: 2rem;
    text-shadow:
        0.5px 0 0 currentColor,
        -0.5px 0 0 currentColor,
        0 0.5px 0 currentColor,
        0 -0.5px 0 currentColor;

    border: 1px solid #DCB482;
    &:hover {
        border: 1px solid #DCB482;
        box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.43) inset;
        -webkit-box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.43) inset;
        -moz-box-shadow: 10px -25px 81px 7px rgba(0,0,0,0.43) inset;
    }

    @media (max-width: 1280px) { 
        width: 300px;
        font-size: 1.5rem;
    }
    
    @media (max-width: 1024px) { 
        width: 200px;
        font-size: 1.2rem;
    }
    
    @media (max-width: 630px) {
        font-size: 1rem;
    }
  }
`;
