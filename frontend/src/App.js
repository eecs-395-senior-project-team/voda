import React, { Component } from 'react';
import './App.sass';
import Map from './Map';
import Header from './Header';
import Footer from './Footer';
import Popup from './Popup';
import Detail from './Detail';

/**
 * Top level application component
 */
class App extends Component {
  constructor(props) {
    super(props);
    this.hidePopup = this.hidePopup.bind(this);
    this.showPopup = this.showPopup.bind(this);
    this.hideDetail = this.hideDetail.bind(this);
    this.showDetail = this.showDetail.bind(this);
    this.state = {
      popupIsVisible: false,
      detailIsVisible: false,
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

    hideDetail() {
    this.setState({
      detailIsVisible: false
    });
  }

  showDetail() {
    this.setState({
      detailIsVisible: true
    });
  }

  render() {
    const header = 'Voda';
    const footer = 'created by anna, david f, david n, david n || 2019';
    const {
      popupIsVisible,
      detailIsVisible,
      selectedCountyID,
      selectedCountyName,
      selectedStateID,
    } = this.state;
    let popUp;
    let detail;
    if (popupIsVisible) {
      popUp = (
        <Popup
          hidePopup={this.hidePopup}
          countyID={selectedCountyID}
          countyName={selectedCountyName}
          stateID={selectedStateID}/>
      );
    } else {
      popUp = null;
    }
    if (detailIsVisible) {
      detail = (
        <Detail
          hideDetail={this.hideDetail}
          countyID={selectedCountyID}
          countyName={selectedCountyName}
          stateID={selectedStateID}/>
      );
    } else {
      detail = null;
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
