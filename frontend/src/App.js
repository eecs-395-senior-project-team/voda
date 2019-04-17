import React, { Component } from 'react';
import './App.css';

const axios = require('axios');

/** Class that handles small popup when a district is clicked */
class Popup extends React.Component {
  render() {
    return ( 
      <div className='popup'>
        <div className='popup_inner'>
          <div className='header_popup'>
            <p>{this.props.header}</p>
          </div>
          <p>{this.props.text}</p>
          <button className = "square2" onClick={this.props.closePopup}>Back</button>
          <button className = "square2" onClick={this.props.toggleFullView}>More</button>
        </div>
      </div>
    );
  }
}

/** Class that handles small popup when a district is clicked */
class FullView extends React.Component {
  render() {
    return (
      <div className='full_view'>
        <div className='full_view_inner'>
          <p>{this.props.header}</p>
          <div className = 'full_view_paragraph'>
            <p>{this.props.text}</p>
          </div>
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
      text: '',
      header: '',
      map: null,
      data: [],
      selectedState: '',
    };
    this.togglePopupRegion = this.togglePopupRegion.bind(this)
    this.toggleFullViewRegion = this.toggleFullViewRegion.bind(this)
  }

  /* Updates map on startup*/
  componentWillMount() {

     //to be executed when JSON file imported from backend
    axios.get('http://localhost:8000/map').then(function(response) {
      console.log(response);
      this.setState( {
        data: response.data
      }) 
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
  * Changes the state of the popup and gets backend info
  */
  togglePopupRegion(state) {
    axios.get('http://localhost:8000/summary', {
      params: {
        source: this.state.selectedState
      }
    }).then(function(response) {
      
      //over write text on summary
      var text2 = response.data
      console.log(text2)
      this.setState({
        text: text2
      })
    }.bind(this))
    .catch (function (error){
      console.log(error);
    });

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
  * Changes the state of the popup and gets backend info
  */

  toggleFullViewRegion(state) {
    axios.get('http://localhost:8000/details', {
      params: {
        source: this.state.selectedState
      }
    }).then(function(response) {
      
      // over write text on detail
      var text3 = response.data
      console.log(text3)
      this.setState({
        text: text3
      })

    }.bind(this))
    .catch (function (error){
      console.log(error);
    });

    this.setState({
      showPopup: !this.state.showPopup,
      showFullView: !this.state.showFullView
    });
  } 

  /**
  * Fully renders the application
  */
  render() {

    //header
    const title = 'voda';

    //footer
    const footer = 'created by anna, david n, david n, david f || 2019'

    // event listener for map
    const chartEvents = [{
      eventName: "regionClick",
      callback( {chartWrapper} ) {
        console.log("region clicked");
      }
    }];

    // options  for map
    const options = {
      region: 'US',  // the US region
      resolution: 'provinces',
      colorAxis: { colors: ['#CAE4DB', '7A9D96', '#00303F'] },
      datalessRegionColor: '#edeae5',
      defaultColor: '#f5f5f5',
      enableRegionInteractivity: true //to interact with regions
    };

    return (
      <div className = "App">
        <div className ="header"> {title} </div>
        <div className = "map">
        <div style={{ height: '500px', width: '1000px' }}>
        <GoogleMapReact
          bootstrapURLKeys={{ key:'AIzaSyDPQzcjtqG88UJbV2_mv3zSfVMWBqYeue8'}}
          defaultCenter={{lat: 41.850033, lng: -87.6500523} }
          defaultZoom={4}>

        </GoogleMapReact>
        </div>
        </div>
        {this.state.showPopup ? 
          <Popup
            header='Summary'
            text={this.state.text}
            closePopup={this.togglePopup.bind(this)}
            toggleFullView ={this.toggleFullViewRegion.bind(this)} />
          : null
        }
        {this.state.showFullView ? 
          <FullView
            header='VODA'
            text={this.state.text}
            closeFullView ={this.toggleFullView.bind(this)} />
          : null
        }
        <div className ="footer"> {footer} </div>
      </div>
    );
  }
}

export default App;
