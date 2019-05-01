import React, { Component } from 'react';
import PropTypes from 'prop-types';
import './TabDetails.sass';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import TabContainer from 'react-bootstrap/TabContainer';
import TabContent from 'react-bootstrap/TabContent';
import TabPane from 'react-bootstrap/TabPane';
import Table from 'react-bootstrap/Table';
import Axios from 'axios';
import ContaminantList from './ContaminantList';
import Log from './Log';

/**
 * A set of tab components for a Detail View
 */
class TabDetails extends Component {
  constructor(props) {
    super(props);
    this.setCurrentContaminant = this.setCurrentContaminant.bind(this);
    this.state = {
      contaminantDetails: {
        'Amount in water': 0,
        'Health Guideline': 0,
        'Legal Limit': 0,
        Details: '',
      },
    };
  }

  setCurrentContaminant(selectedContaminant) {
    const { sourceID } = this.props;
    let apiURL;
    if (process.env.NODE_ENV === 'development') {
      apiURL = 'http://localhost:8000/';
    } else {
      apiURL = 'http://3.19.113.236:8000/';
    }
    const url = `${apiURL}contaminantInfo`;
    Axios.get(url, {
      params: {
        source: sourceID,
        contaminant: selectedContaminant,
      },
    })
      .then((contaminantInfoResponse) => {
        const contaminantDetails = contaminantInfoResponse.data;
        this.setState({ contaminantDetails });
      })
      .catch((error) => {
        Log.error(error, 'Tab Component');
      });
  }

  render() {
    const { contaminantDetails } = this.state;
    const { contaminants } = this.props;
    const tabPanes = [];
    for (let i = 0; i < contaminants.length; i += 1) {
      tabPanes.push(
        <TabPane
          key={`#pane-key-${i}`}
          eventKey={`#item${i}`}
        >
          <div className="pane-body">
            <Table responsive borderless="true">
              <tbody>
                <tr>
                  <td>
                    <h5>
                      <div className="SmallHeader">
                        Amount in water:
                      </div>
                    </h5>
                  </td>
                  <td>
                    <h5>
                      <div className="SmallHeader">
                        Health Guideline:
                      </div>
                    </h5>
                  </td>
                  <td>
                    <h5>
                      <div className="SmallHeader">
                        Legal Limit:
                      </div>
                    </h5>
                  </td>
                </tr>
                <tr>
                  <td>
                    <div className="Numbers">
                      {contaminantDetails['Amount in water']}
                      <span className="unit"> ppb</span>
                    </div>
                  </td>
                  <td>
                    <div className="Numbers">
                      {contaminantDetails['Health Guideline']}
                      <span className="unit"> ppb</span>
                    </div>
                  </td>
                  <td>
                    <div className="Numbers">
                      {contaminantDetails['Legal Limit']}
                      <span className="unit"> ppb</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </Table>
            <p>
              {contaminantDetails.Details}
            </p>
          </div>
        </TabPane>,
      );
    }
    return (
      <TabContainer
        mountOnEnter
      >
        <Row>
          <Col sm={4}>
            <div className="contaminant-list">
              <ContaminantList
                contaminants={contaminants}
                setCurrentContaminant={this.setCurrentContaminant}
              />
            </div>
          </Col>
          <Col sm={8}>
            <TabContent>
              {tabPanes}
            </TabContent>
          </Col>
        </Row>
      </TabContainer>
    );
  }
}
TabDetails.propTypes = {
  contaminants: PropTypes.arrayOf(String).isRequired,
  sourceID: PropTypes.string.isRequired,
};

export default TabDetails;
