import { useState, type JSX } from "react";
import { Form, Input, SearchButton } from "./SearchBar.styles";


interface SearchBarProps {
    onSearch: (query: string) => void;
}

const SearchBar = ({ onSearch }: SearchBarProps): JSX.Element => {
  const [query, setQuery] = useState("");

  const handleSearch = (value: string) => {
    setQuery(value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSearch(query);
    query && onSearch(query);
    clearSearch();
  };

  const clearSearch = () => {
    setQuery("");
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Input
        type="text"
        placeholder="What book are you look for today..."
        value={query}
        onChange={(e) => handleSearch(e.target.value)}
      />

      <SearchButton type="submit">Recall</SearchButton>
    </Form>
  );
}

export default SearchBar;