import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Axios from 'axios';
import './DetailView.sass';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';
import TabDetails from './TabDetails';
import Log from './Log';

/**
 * DetailView Component.
 */
class DetailView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeTab: 'red',
      redContaminants: ['a', 'b'],
      yellowContaminants: ['c', 'd'],
      greenContaminants: ['e', 'f'],
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
    const {
      activeTab,
      redContaminants,
      yellowContaminants,
      greenContaminants,
    } = this.state;
    const {
      hideDetailView,
      countyName,
      countyID,
      stateID,
    } = this.props;
    const redIcon = <i className="fas fa-exclamation-triangle" />;
    const yellowIcon = <i className="fas fa-notes-medical" />;
    const greenIcon = <i className="fas fa-check" />;

    return (
      <div class = "card-body d-flex flex-column">
        <div className="Details border border-dark rounded">
          <h1>
            {`Contaminant Details For ${countyName} County`}
          </h1>
          <Tabs
            className = "classOne"
            activeKey={activeTab}
            onSelect={key => this.setState({ activeTab: key })}
          >
            <Tab eventKey="red" title={redIcon}>
              <TabDetails
                contaminants={redContaminants}
                countyID={countyID}
                stateID={stateID}
              />
            </Tab>

            <Tab eventKey="profile" title={yellowIcon}>
              <TabDetails
                contaminants={yellowContaminants}
                countyID={countyID}
                stateID={stateID}
              />
            </Tab>
            <Tab eventKey="contact" title={greenIcon}>
              <TabDetails
                contaminants={greenContaminants}
                countyID={countyID}
                stateID={stateID}
              />
            </Tab>
          </Tabs>
          <hr />
            <button type="button" class="float-right align-self-end flex-grow d-flex align-items-end btn btn-secondary" onClick={hideDetailView}>
              Close
            </button>
        </div>
      </div>
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
