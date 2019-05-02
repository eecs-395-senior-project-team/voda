import React, { Component } from 'react';
import './App.sass';
import Map from './Map';
import Header from './Header';
import Footer from './Footer';
import Popup from './Popup';
import DetailView from './DetailView';

/**
 * Top level application component
 */
class App extends Component {
  constructor(props) {
    super(props);
    this.hideDetailView = this.hideDetailView.bind(this);
    this.showDetailView = this.showDetailView.bind(this);
    this.hidePopup = this.hidePopup.bind(this);
    this.showPopup = this.showPopup.bind(this);
    this.state = {
      detailViewIsVisible: false,
      popupIsVisible: false,
      selectedCountyName: '',
      selectedSourceID: '',
    };
  }

  hideDetailView() {
    this.setState({
      detailViewIsVisible: false,
      selectedCountyName: '',
      selectedSourceID: '',
    });
  }

  showDetailView() {
    this.setState({
      detailViewIsVisible: true,
      popupIsVisible: false,
    });
  }

  hidePopup() {
    this.setState({
      popupIsVisible: false,
      selectedCountyName: '',
      selectedSourceID: '',
    });
  }

  showPopup(countyName, sourceID) {
    this.setState({
      popupIsVisible: true,
      selectedCountyName: countyName,
      selectedSourceID: sourceID,
    });
  }

  render() {
    const header = 'Voda';
    const footer = 'created by anna, david, david, david || 2019';
    const {
      detailViewIsVisible,
      popupIsVisible,
      selectedCountyName,
      selectedSourceID,
      contaminantColors,
    } = this.state;
    let popUp;
    if (popupIsVisible) {
      popUp = (
        <Popup
          showDetailView={this.showDetailView}
          hidePopup={this.hidePopup}
          countyName={selectedCountyName}
          sourceID={selectedSourceID}
        />
      );
    } else {
      popUp = null;
    }
    let content;
    if (detailViewIsVisible) {
      content = (
        <DetailView
          hideDetailView={this.hideDetailView}
          countyName={selectedCountyName}
          sourceID={selectedSourceID}
        />
      );
    } else {
      content = (
        <div>
          <Map showPopup={this.showPopup} contaminantColors={contaminantColors} />
          {popUp}
        </div>
      );
    }
    return (
      <div className="App container-fluid">
        <Header header={header} />
        <div className="row justify-content-center">
          <div className="col-xs-12 content">
            {content}
          </div>
        </div>
        <Footer footer={footer} />
      </div>
    );
  }
}

export default App;
