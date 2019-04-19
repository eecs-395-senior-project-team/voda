import React, { Component } from 'react';
import L from 'leaflet';
import Axios from 'axios';
import PropTypes from 'prop-types';
import './Map.sass';
import Alert from './Alert';
import Log from './Log';

const countiesJson = require('./data/counties_20m.json');

/**
 * Component containing the geomap.
 */
class Map extends Component {
  constructor(props) {
    super(props);
    this.mapboxAccessToken = 'pk.eyJ1Ijoidm9kYSIsImEiOiJjanU0bXR6NXIwemxoNDRxdm9wMTc2YTd5In0.Z3LcZt3raPAfcQan-k59XQ';
    this.state = {
      counties: countiesJson,
      lat: 37.8,
      lng: -96,
      zoom: 4,
      browserAlert: false,
    };
  }

  // Initializes map colors
  componentWillMount() {
    Axios.get('http://localhost:8000/map')
      .then((response) => {
        Log.info(response, 'Map Component');
      })
      .catch((error) => {
        Log.error(error, 'Map Component');
      });
  }

  // Enable Map
  componentDidMount() {
    const {
      lat, lng, zoom, counties,
    } = this.state;
    this.map = L.map('map', {
      center: [lat, lng],
      zoom,
      minZoom: 4,
      maxZoom: 10,
      zoomSnap: 1,
      wheelDebounceTime: 10,
      maxBounds: L.latLngBounds(
        L.latLng(-4, -55),
        L.latLng(71.6, -180),
      ),
      layers: [
        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
          attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
          id: 'mapbox.light',
          accessToken: this.mapboxAccessToken,
        }),
      ],
    });
    let geoJson;
    const highlightFeature = (e) => {
      const selectedLayer = e.target;
      selectedLayer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7,
      });
      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        selectedLayer.bringToFront();
      } else {
        this.setState({
          browserAlert: true,
        });
      }
    };
    const resetHighlight = (e) => {
      geoJson.resetStyle(e.target);
    };
    const zoomToFeature = (e) => {
      const { showPopup } = this.props;
      this.map.fitBounds(e.target.getBounds());
      const {
        COUNTY,
        NAME,
        STATE,
      } = e.target.feature.properties;
      Log.info(e.target.feature.properties, 'Map Component');
      showPopup(COUNTY, NAME, STATE);
    };
    geoJson = L.geoJson(counties, {
      style() {
        return {
          fillColor: '#800026',
          weight: 1,
          opacity: 0.5,
          color: 'black',
          dashArray: '',
          fillOpacity: 0.7,
        };
      },
      onEachFeature(feature, layer) {
        layer.on({
          mouseover: highlightFeature,
          mouseout: resetHighlight,
          click: zoomToFeature,
        });
      },
    }).addTo(this.map);
  }

  render() {
    const { browserAlert } = this.state;
    let alert;

    if (browserAlert) {
      alert = <Alert message="Sorry! Your browser is not supported!" />;
    } else {
      alert = null;
    }

    return (
      <div>
        {alert}
        <div className="Map border border-dark rounded" id="map" />
      </div>
    );
  }
}
Map.propTypes = {
  showPopup: PropTypes.func.isRequired,
};

export default Map;
