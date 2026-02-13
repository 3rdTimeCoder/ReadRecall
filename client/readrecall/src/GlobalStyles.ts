// GlobalStyle.js
import { createGlobalStyle } from 'styled-components';

export const GlobalStyle = createGlobalStyle`
  /* Apply box-sizing and resets */
  *, *::before, *::after {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: 'Almendra Display', serif; /* Default body font */
    line-height: 1.6;
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: 'UnifrakturMaguntia', cursive;
    margin-top: 0;
    margin-bottom: 1rem;
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
`;
