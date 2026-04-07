import React from 'react';
import "./header.css";

const Header: React.FC = () => {
  return (
    <header>
      <nav>
        <a href="/">Home</a> | <a href="/about">About</a>
      </nav>
    </header>
  );
}

export default Header;