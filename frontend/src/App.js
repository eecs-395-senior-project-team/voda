import React, { Component } from 'react';
import './App.sass';
import Map from './Map';
import Header from './Header';
import Footer from './Footer';
import Popup from './Popup';

/**
 * Top level application component
 */
class App extends Component {
  constructor(props) {
    super(props);
    this.hidePopup = this.hidePopup.bind(this);
    this.showPopup = this.showPopup.bind(this);
    this.state = {
      popupIsVisible: false,
      selectedCountyID: '',
      selectedCountyName: '',
      selectedStateID: '',
    };
  }

  hidePopup() {
    this.setState({
      popupIsVisible: false,
      selectedCountyID: '',
      selectedCountyName: '',
      selectedStateID: '',
    });
  }

  showPopup(countyID, countyName, stateID) {
    this.setState({
      popupIsVisible: true,
      selectedCountyID: countyID,
      selectedCountyName: countyName,
      selectedStateID: stateID,
    });
  }

  render() {
    const header = 'Voda';
    const footer = 'created by anna, david f, david n, david n || 2019';
    const {
      popupIsVisible,
      selectedCountyID,
      selectedCountyName,
      selectedStateID,
    } = this.state;
    let popUp;
    if (popupIsVisible) {
      popUp = (
        <Popup
          hidePopup={this.hidePopup}
          countyID={selectedCountyID}
          countyName={selectedCountyName}
          stateID={selectedStateID}
        />
      );
    } else {
      popUp = null;
    }
    return (
      <div className="App container-fluid">
        <Header header={header} />
        <div className="row justify-content-center">
          <div className="col-xs-12 content">
            <Map showPopup={this.showPopup} />
            {popUp}
          </div>
        </div>
        <Footer footer={footer} />
      </div>
    );
  }
}

export default App;
