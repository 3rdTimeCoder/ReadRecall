import styled from "styled-components";

export const Form = styled.form`
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
  padding: 1rem 2rem;

  @media (max-width: 868px) {
    flex-direction: column;
  }

  @media (max-width: 630px) {
    padding: 0;
  }
`;

export const Input = styled.input`
  padding: 10px 14px;
  font-size: 18px;
  border-radius: 40px;
  border: 1px solid #DCB482;
  font-size: 1.2rem;
  color: #DCB482;
  padding: 1rem;
  width: 650px;
  max-width: 100;
  max-width: 80%;
  outline: none;
  background: #111;
  z-index: 100;

  &:focus {
    border: 2px solid #DCB482;
  }

  @media (max-width: 1280px) {
  }

  @media (max-width: 1024px) {}

  @media (max-width: 768px) {
    font-size: 1rem;
    width: 450px;
  }

  @media (max-width: 630px) {
    width: 360px;
  }

  @media (max-width: 410px) {
    width: 350px;
  }
`;

export const SearchButton = styled.button`
  width: 150px;
  font-size: 1.4rem;

  @media (max-width: 768px) {
    font-size: 1rem;
  }

  @media (max-width: 630px) {
    width: 110px;
  }
`;

