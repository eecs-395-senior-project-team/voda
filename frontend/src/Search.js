import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Axios from 'axios';
import './Search.sass';
import Form from 'react-bootstrap/Form';
import Log from './Log';
import Alert from './Alert';

/**
 * Searchbar Component
 */
class Search extends Component {
  constructor(props) {
    super(props);
    this.state = {
      displayAlert: false,
      query: '',
    };
  }

  search(e) {
    const { query } = this.state;
    const { showPopup, changeMapColor } = this.props;
    e.preventDefault();
    let apiURL;
    if (process.env.NODE_ENV === 'development') {
      apiURL = 'http://localhost:8000/';
    } else {
      apiURL = 'http://3.19.113.236:8000/';
    }
    const url = `${apiURL}search`;
    Axios.get(url, {
      params: { query },
    })
      .then((response) => {
        if (response.data.type === 'source') {
          const { countyName, sourceID } = response.data.data;
          showPopup(countyName, sourceID);
        } else if (response.data.type === 'contaminant') {
          const { data } = response.data;
          changeMapColor(data);
        }
      })
      .catch((error) => {
        Log.error(error, 'search');
        this.setState({ displayAlert: true });
      });
  }

  render() {
    const { displayAlert } = this.state;
    const setQuery = (e) => {
      this.setState({ query: e.target.value, displayAlert: false });
    };
    let alert;
    if (displayAlert) {
      alert = (
        <Alert className="full-width" message="Search not found" />
      );
    } else {
      alert = null;
    }
    return (
      <div>
        <Form onKeyDown={
            (e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                this.search(e);
              }
            }
          }
        >
          <Form.Group controlId="formSearch">
            <Form.Control
              type="text"
              placeholder="Search Voda"
              onChange={setQuery}
            />
          </Form.Group>
        </Form>
        {alert}
      </div>
    );
  }
}
Search.propTypes = {
  showPopup: PropTypes.func.isRequired,
  changeMapColor: PropTypes.func.isRequired,
};

export default Search;
