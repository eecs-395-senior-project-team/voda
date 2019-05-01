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
      redContaminants: [],
      yellowContaminants: [],
      greenContaminants: [],
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
    const url = `${apiURL}contaminants`;
    Axios.get(url, {
      params: {
        source: `${stateID}${countyID}`,
      },
    })
      .then((contaminants) => {
        const {
          redContaminants,
          yellowContaminants,
          greenContaminants,
        } = contaminants.data
        this.setState({
          redContaminants,
          yellowContaminants,
          greenContaminants,
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
      <div className="Details border border-dark rounded">
        <h1>
          {`Contaminant Details For ${countyName} County`}
        </h1>
        <Tabs
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
        <div className="closeButton">
          <button type="button" className="btn btn-secondary" onClick={hideDetailView}>
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
