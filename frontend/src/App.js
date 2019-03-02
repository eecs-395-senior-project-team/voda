import React, { Component } from 'react';
import GoogleMapReact from 'google-map-react';
import './App.css';
import $ from 'jquery'; 

const axios = require('axios');

/** Class that handles small popup when a district is clicked */
class Popup extends React.Component {
  render() {
    return (
      <div className='popup'>
        <div className='popup_inner'>
          <p>{this.props.text}</p>
          <button onClick={this.props.closePopup}>Back</button>
          <button onClick={this.props.toggleFullView}>More Details</button>
        </div>
      </div>
    );
  }
}

/** Class that handles small popup when a district is clicked */
class FullView extends React.Component {
  render() {
    return (
      <div className='full_view'>i
        <div className='full_view_inner'>
          <p>{this.props.text}</p>

          // goes back to the main page
          <button className = "square" onClick={this.props.closeFullView}>Back</button>
        </div>
      </div>
    )
  }
}

/** Map implementation for the front page */
class SimpleMap extends React.Component {
  static defaultProps = {
    center: {
      lat: 59.95,
      lng: 30.33
    },
    zoom: 11
  };
 
  render() {
    return (

      // Important! Always set the container height explicitly
      <div style={{ height: '100vh', width: '100%' }}>
        <GoogleMapReact
          //bootstrapURLKeys={{ key: /* YOUR KEY HERE */ }}
          defaultCenter={this.props.center}
          defaultZoom={this.props.zoom}
        >
        </GoogleMapReact>
      </div>
    );
  }
}

// Main class
class App extends Component {

/**
 * Manages the state of the popup components
 * @constructor
 */
  constructor(props) {
    super(props);
    this.state = {
      value: null,
      showPopup: false,
      showFullView: false,
      map: null
    };
    this.popupInfo = this.popupInfo.bind(this)
    this.fullViewInfo = this.fullViewInfo.bind(this)
  }

  /* Updates map on startup*/
  componentWillMount() {
    axios.get('localhost:3500/map').then(function(response) {
      console.log(response);
      /**
      * get data from response
      * this.setState({map: response})
      **/
    })
    .catch (function (error){
      console.log(error);
    })
    .then (function (){
      //always executed
    });
  }

  /* Gets info for the popup*/
  popupInfo() {
    axios.get('localhost:3500/summary').then(function(response) {
      console.log(response);
      /**
      * get data from response
      * this.setState({map: response})
      **/
    })
    .catch (function (error){
      console.log(error);
    })
    .then (function (){
      //always executed
    });
  }

  /* Gets info for the fullview*/
  fullViewInfo() {
    axios.get('localhost:3500/details').then(function(response) {
      console.log(response);
      /**
      * get data from response
      * this.setState({map: response})
      **/
    })
    .catch (function (error){
      console.log(error);
    })
    .then (function (){
      //always executed
    });
  }

  /**
  * Changes the state of the popup
  */
  togglePopup() {
    this.setState({
      showPopup: !this.state.showPopup
    });
  }

  /**
  * Changes the state of the full view
  */
  toggleFullView() {
    this.setState({
      showPopup: !this.state.showPopup,
      showFullView: !this.state.showFullView
    });
  }

  /**
  * Fully renders the application
  */
  render() {
    const status = 'voda';
    return (
      <div className = "App">
        <div className ="header"> {status} </div>
        <button className = "square" onClick={this.togglePopup.bind(this)}>Show</button>
        {this.state.showPopup ? 
          <Popup
            text='Contaminents Detail'
            closePopup={this.togglePopup.bind(this)}
            toggleFullView ={this.toggleFullView.bind(this)} />
          : null
        }
        {this.state.showFullView ? 
          <FullView
            text='VODA'
            closeFullView ={this.toggleFullView.bind(this)} />
          : null
        }
      </div>
    );
  }
}

export default App;
