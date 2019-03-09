import React, { Component } from 'react';
import { render } from "react-dom";
import { Chart } from "react-google-charts";
import './App.css';
var fs = require("fs");

const axios = require('axios');

//read a JSON file
var content = fs.readFile("keys.JSON");
var key = JSON.parse(content);

/* 
* Load a specific type(s) of chart(s). You can call this as many times as you need from anywhere in your app
* GoogleCharts is a singleton and will not allow the script to be loaded more than once
* The mapsApiKey is only required for certain GeoCharts
*/

GoogleCharts.load(drawGeoChart, {
    'packages': ['geochart'],
    'mapsApiKey': key.API_KEY
});


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
    axios.get('http://localhost:8000/map').then(function(response) {
      console.log(response);
      /**
      * get data from response
      * this.setState({map: response})
      **/

      //this is the part where we setup the map

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
    axios.get('http://localhost:8000/summary').then(function(response) {
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
    axios.get('http://localhost:8000/details').then(function(response) {
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
        <div className={"my-pretty-chart-container"}>
        <Chart
          chartType="ScatterChart"
          data={[["Age", "Weight"], [4, 5.5], [8, 12]]}
          width="100%"
          height="400px"
          legendToggle
        />
        </div>

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
