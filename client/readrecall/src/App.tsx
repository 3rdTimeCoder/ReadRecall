import { useState, type JSX } from 'react';
import { AppContainer, BookBackground, BookVector, BookVectorContainer } from './App.styles';
import { ThemeProvider } from 'styled-components';
import { japandiDark } from './lib/theme/theme';
import { GlobalStyle } from './GlobalStyles';
import SearchBar from './search-bar/SearchBar';


interface AppProps {}


function App({}: AppProps): JSX.Element {
   const [results, setResults] = useState();

   const handleSearch = (query: string) => {}

  return (
    <ThemeProvider theme={japandiDark}>
      <GlobalStyle />
      <AppContainer>
        <BookBackground />
        <BookVectorContainer>
          <BookVector />
        </BookVectorContainer>
        <h1>ReadRecall</h1>

        <div style={{ padding: "40px" }}>
          <SearchBar onSearch={handleSearch} />

          {/* <ul style={{ marginTop: "20px" }}>
            {results.map((book, index) => (
              <li key={index}>{book}</li>
            ))}
          </ul> */}
        </div>
      </AppContainer>
    </ThemeProvider>
  )
}

export default App;
