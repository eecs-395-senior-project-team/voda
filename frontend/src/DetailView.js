import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Axios from 'axios';
import Log from './Log';
import './DetailView.sass';

/**
 * DetailView Component.
 */
class DetailView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      details: '',
    };
  }

  componentWillMount() {
    const { countyID, stateID } = this.props;
    let apiURL;
    if (process.env.NODE_ENV === 'development') {
      apiURL = 'http://localhost:8000/';
    } else {
      apiURL = 'http://3.19.113.236:8000/';
    }
    const url = `${apiURL}details`;
    Axios.get(url, {
      params: {
        source: `${stateID}${countyID}`,
      },
    })
      .then((details) => {
        this.setState({
          details: details.data,
        });
      })
      .catch((error) => {
        Log.error(error, 'Details Component');
      });
  }

  render() {
    const { details } = this.props;
    const { hideDetailView, countyName } = this.props;
    return (
      <div className="Details border border-dark rounded">Place Detail View Here</div>
    );
  }
}

DetailView.propTypes = {
  hideDetailView: PropTypes.func.isRequired,
  countyID: PropTypes.string.isRequired,
  countyName: PropTypes.string.isRequired,
  stateID: PropTypes.string.isRequired,
};

export default DetailView;
