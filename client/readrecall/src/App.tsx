import { useState, type JSX } from 'react';
import { AppContainer, BookBackground, BookVector, BookVectorContainer, Logo, MainLayout } from './App.styles';
import { ThemeProvider } from 'styled-components';
import { japandiDark } from './lib/theme/theme';
import { GlobalStyle } from './GlobalStyles';
// import SearchBar from './components/recall/search-bar/SearchBar';
import FileUploader from './components/ingest/file-uploader/FileUploader';
import Recall from './components/recall/Recall';


interface AppProps {}


function App({}: AppProps): JSX.Element {
   const [results, setResults] = useState();

   const handleSearch = (query: string) => {}

  return (
    <ThemeProvider theme={japandiDark}>
      <GlobalStyle />
      <AppContainer>
        <Logo><h1>ReadRecall</h1></Logo>
        <BookBackground />
          <BookVectorContainer>
            <BookVector />
          </BookVectorContainer>
          {/* <FileUploader onUpload={() => {}} /> */}
          <Recall />

      </AppContainer>
    </ThemeProvider>
  )
}

export default App;
