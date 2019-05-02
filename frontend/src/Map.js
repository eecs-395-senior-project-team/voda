import React, { Component } from 'react';
import L from 'leaflet';
import Axios from 'axios';
import PropTypes from 'prop-types';
import Color from 'color';
import './Map.sass';
import Alert from './Alert';
import Log from './Log';
import Search from './Search';

// Axios get request for counties
const getCounties = () => Axios.get('https://s3.us-east-2.amazonaws.com/voda-counties-data/data/counties_20m.json');

// Axios get request for scores
let getScores;
if (process.env.NODE_ENV === 'development') {
  getScores = () => Axios.get('http://localhost:8000/map');
} else {
  getScores = () => Axios.get('http://3.19.113.236:8000/map');
}

const scale = (val, minScore) => Math.log(val / 50 + (1 - minScore / 50));

/**
 * Component containing the geomap.
 */
class Map extends Component {
  constructor(props) {
    super(props);
    this.changeMapColor = this.changeMapColor.bind(this);
    this.resetMap = this.resetMap.bind(this);
    this.mapboxAccessToken = 'pk.eyJ1Ijoidm9kYSIsImEiOiJjanU0bXR6NXIwemxoNDRxdm9wMTc2YTd5In0.Z3LcZt3raPAfcQan-k59XQ';
    this.state = {
      counties: {},
      map: {},
      lat: 37.8,
      lng: -96,
      zoom: 4,
      browserAlert: false,
      minScore: Infinity,
      trueMinScore: null,
      maxScore: -Infinity,
      trueMaxScore: null,
      geoLayer: null,
      trueCounties: {},
    };
  }

  // Initializes map colors
  componentWillMount() {
    Axios.all([getCounties(), getScores()])
      .then(Axios.spread((countiesResponse, scoresResponse) => {
        const counties = countiesResponse.data;
        const { scores, sourceIDs } = scoresResponse.data;
        const { minScore, maxScore } = this.state;
        let newMinScore = minScore;
        let newMaxScore = maxScore;
        for (let i = 0; i < counties.features.length; i += 1) {
          const fipsCode = `${counties.features[i].properties.STATE}${counties.features[i].properties.COUNTY}`;
          if (fipsCode in scores) {
            counties.features[i].properties.SCORE = scores[fipsCode];
            counties.features[i].properties.SOURCEID = sourceIDs[fipsCode];
            if (scores[fipsCode] < newMinScore) {
              newMinScore = scores[fipsCode];
            }
            if (scores[fipsCode] > newMaxScore) {
              newMaxScore = scores[fipsCode];
            }
          } else {
            counties.features[i].properties.SCORE = -Infinity;
          }
        }
        this.setState({
          counties,
          minScore: newMinScore,
          trueMinScore: minScore,
          maxScore: newMaxScore,
          trueMaxScore: maxScore,
          trueCounties: JSON.parse(JSON.stringify(counties))
        });
      }))
      .catch((error) => {
        Log.error(error, 'Map Component');
      });
  }

  // Enable Map
  componentDidMount() {
    const {
      lat,
      lng,
      zoom,
    } = this.state;
    this.setState(
      {
        map: L.map(
          'map',
          {
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
          },
        ),
      },
    );
  }

  // Move to ComponentWillMount
  componentDidUpdate(_, prevState) {
    const {
      counties,
      map,
      minScore,
      maxScore,
    } = this.state;
    let { counties: prevCounties } = prevState;
    if (typeof prevCounties === 'undefined') {
      prevCounties = { features: [] };
    }
    // When counties change
    if (
      counties.features !== prevCounties.features
      && Object.entries(counties).length !== 0
      && counties.constructor === Object
    ) {
      let geoJson;
      const getColor = (score) => {
        if (score === -Infinity) {
          return '#ffffff';
        }
        const value = (
          (scale(score, minScore) - scale(minScore, minScore))
          / (scale(maxScore, minScore) - scale(minScore, minScore))
          * (100));
        const hue = Math.floor((100 - value) * 120 / 100);
        return Color({ h: hue, s: 100, v: 100 }).hex();
      };
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
        map.fitBounds(e.target.getBounds());
        const {
          NAME,
          SOURCEID,
        } = e.target.feature.properties;
        showPopup(NAME, SOURCEID);
      };
      geoJson = L.geoJson(counties, {
        style(feature) {
          return {
            fillColor: getColor(feature.properties.SCORE),
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
      });
      this.setState({
        map: map.addLayer(geoJson),
        geoLayer: geoJson,
      });
    }
  }

  changeMapColor(data) {
    const { counties, geoLayer, map } = this.state;
    let newCounties = JSON.parse(JSON.stringify(counties))
    let newMinScore = Infinity;
    let newMaxScore = -Infinity;
    for (let i = 0; i < newCounties.features.length; i += 1) {
      const fipsCode = `${newCounties.features[i].properties.STATE}${newCounties.features[i].properties.COUNTY}`;
      if (fipsCode in data) {
        newCounties.features[i].properties.SCORE = data[fipsCode];
        if (data[fipsCode] < newMinScore) {
          newMinScore = data[fipsCode];
        }
        if (data[fipsCode] > newMaxScore) {
          newMaxScore = data[fipsCode];
        }
      } else {
        newCounties.features[i].properties.SCORE = -Infinity;
      }
    }
    this.setState({
      counties: newCounties,
      minScore: newMinScore,
      maxScore: newMaxScore,
      map: map.removeLayer(geoLayer),
      geoLayer: null,
    });
  }

  resetMap() {
    const { trueCounties, trueMaxScore, trueMinScore, geoLayer, map } = this.state;
    this.setState({
      counties: trueCounties,
      minScore: trueMinScore,
      maxScore: trueMaxScore,
      map: map.removeLayer(geoLayer),
      geoLayer: null,
    });
  }

  render() {
    const { browserAlert } = this.state;
    const { showPopup } = this.props;
    let alert;

    if (browserAlert) {
      alert = <Alert message="Sorry! Your browser is not supported!" />;
    } else {
      alert = null;
    }

    return (
      <div>
        {alert}
        <div className="search col-sm-8">
          <Search 
            showPopup={showPopup} changeMapColor={this.changeMapColor} />
        </div>
        <div className="Map border border-dark rounded" id="map" />
      </div>
    );
  }
}
Map.propTypes = {
  showPopup: PropTypes.func.isRequired,
};

export default Map;
