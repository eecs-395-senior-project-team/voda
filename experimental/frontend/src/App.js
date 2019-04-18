import React from 'react';
import './App.css';
import Map from './Map';
import Header from './Header';
import Footer from './Footer';

/**
 * Top level application function
 */
function App() {
  const header = 'Voda';
  const footer = 'created by anna, david f, david n, david n || 2019';

  return (
    <div className="App container-fluid">
      <Header header={header} />
      <Map />
      <Footer footer={footer} />
    </div>
  );
}

export default App;
