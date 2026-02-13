import styled from "styled-components";

export const Form = styled.form`
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
`;

export const Input = styled.input`
  padding: 10px 14px;
  font-size: 18px;
  border-radius: 8px;
  border: 1px solid #ccc;
  width: 650px;
  /* margin-left: 4rem; */
  max-width: 80%;
  outline: none;
  background: transparent;

  &:focus {
    /* border-color: #4f46e5; */
    border: 2px solid #ccc;
  }
`;

export const SearchButton = styled.button`
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  background: #0a0909ae;
  /* color:  */
  cursor: pointer;
  border: 2px solid transparent;
  /* background: #ccc; */

  box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);
-webkit-box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);
-moz-box-shadow: 10px -25px 197px 7px rgba(0,0,0,0.32);

  &:hover {
    opacity: 0.9;
    background: #ccc;
    /* background: #0a0909ae; */
    border: 2px solid transparent;
  }
`;

