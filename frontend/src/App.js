import React, { Component } from 'react';
import GoogleMapReact from 'google-map-react';
import './App.css';

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

class FullView extends React.Component {
  render() {
    return (
      <div className='full_view'>i
        <div className='full_view_inner'>
          <p>{this.props.text}</p>
        <button className = "square" onClick={this.props.closeFullView}>Back</button>
        </div>
      </div>
    )
  }
}

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

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
      showPopup: false,
      showFullView: false
    };
  }

  togglePopup() {
    this.setState({
      showPopup: !this.state.showPopup
    });
  }

  toggleFullView() {
    this.setState({
      showPopup: !this.state.showPopup,
      showFullView: !this.state.showFullView
    });
  }

  render() {
    const status = 'voda';
    return (
      <div className = "App">

        <div className ="header"> 
        {status}
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
