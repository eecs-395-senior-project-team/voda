import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class Popup extends React.Component {
  render() {
    return (
      <div className='popup'>
        <div className='popup_inner'>
          <p>{this.props.text}</p>
        <button onClick={this.props.closePopup}>close me</button>
        </div>
      </div>
    );
  }
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
      showPopup: false
    };
  }

  togglePopup() {
    this.setState({
      showPopup: !this.state.showPopup
    });
  }

  render() {
    const status = 'voda';
    return (
      <div className = "App">

      <div className ="header"> 
      {status}
      </div>
 
        <button className = "square" onClick={this.togglePopup.bind(this)}>show popup</button>
      

        {this.state.showPopup ? 
          <Popup
            text='Contaminents Detail'
            closePopup={this.togglePopup.bind(this)} />
          : null
        }
      </div>
      );
  }
}

export default App;
