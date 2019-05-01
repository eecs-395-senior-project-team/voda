import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Axios from 'axios';
import Modal from 'react-bootstrap/Modal';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Table from 'react-bootstrap/Table';
import Log from './Log';
import './Popup.sass';

/**
 * Popup card component.
 */
class Popup extends Component {
  constructor(props) {
    super(props);
    this.state = {
      summary: '',
      legalLimitConcerns: ['a', 'b', 'c', 'd', 'e'],
      healthGuidelinesConcerns: ['a', 'b', 'c', 'd', 'e', 'f'],
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
    const url = `${apiURL}summary`;
    Axios.get(url, {
      params: {
        source: `${stateID}${countyID}`,
      },
    })
      .then((summary) => {
        this.setState({
          summary: summary.data,
        });
      })
      .catch((error) => {
        Log.error(error, 'Details Component');
      });
  }

  render() {
    const {
      summary,
      legalLimitConcerns,
      healthGuidelinesConcerns,
    } = this.state;
    const {
      showDetailView,
      hidePopup,
      countyName,
    } = this.props;
    const legalLimitTableRows = [];
    let index = 0;
    while (index < legalLimitConcerns.length) {
      const row = [];
      if (legalLimitConcerns.length - index >= 3) {
        for (let i = 0; i < 3; i += 1) {
          row.push(
            <td key={`#col-${i}`}>
              {legalLimitConcerns[index]}
            </td>,
          );
          index += 1;
        }
      } else {
        const remaining = legalLimitConcerns.length - index;
        for (let i = 0; i < remaining; i += 1) {
          row.push(
            <td key={`#col-${i}`}>
              {legalLimitConcerns[index]}
            </td>,
          );
          index += 1;
        }
      }
      legalLimitTableRows.push(
        <tr key={`#row-starting-idx-${index}`}>
          {row}
        </tr>,
      );
    }
    const healthGuidelinesTableRows = [];
    index = 0;
    while (index < healthGuidelinesConcerns.length) {
      const row = [];
      if (healthGuidelinesConcerns.length - index >= 3) {
        for (let i = 0; i < 3; i += 1) {
          row.push(
            <td key={`#col-${i}`}>
              {healthGuidelinesConcerns[index]}
            </td>,
          );
          index += 1;
        }
      } else {
        const remaining = healthGuidelinesConcerns.length - index;
        for (let i = 0; i < remaining; i += 1) {
          row.push(
            <td key={`#col-${i}`}>
              {healthGuidelinesConcerns[index]}
            </td>,
          );
          index += 1;
        }
      }
      healthGuidelinesTableRows.push(
        <tr key={`#row-starting-idx-${index}`}>
          {row}
        </tr>,
      );
    }
    return (
      <Modal
        show
        onHide={hidePopup}
        dialogClassName="popup"
      >
        <Modal.Header closeButton>
          <Modal.Title>
            {`Contaminant Summary For ${countyName} County`}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="container-fluid">
            <div className="row justify-content-center">
              <OverlayTrigger
                overlay={(
                  <Tooltip>
                    Number of contaminants above the legal limit
                  </Tooltip>
                  )}
                placement="top"
              >
                <div className="col-sm-4 bg-danger">
                  <div>
                    <h2><i className="fas fa-exclamation-triangle" /></h2>
                  </div>
                  <h2 className="value">3</h2>
                </div>
              </OverlayTrigger>
              <OverlayTrigger
                overlay={(
                  <Tooltip>
                    Number of contaminants above the health guideline
                  </Tooltip>
                )}
                placement="top"
              >
                <div className="col-sm-4 bg-warning">
                  <div>
                    <h2><i className="fas fa-notes-medical" /></h2>
                  </div>
                  <h2 className="value">8</h2>
                </div>
              </OverlayTrigger>
              <OverlayTrigger
                overlay={(
                  <Tooltip>
                    Number of contaminants that meet the health guideline
                  </Tooltip>
                )}
                placement="top"
              >
                <div className="col-sm-4 bg-success">
                  <div>
                    <h2><i className="fas fa-check" /></h2>
                  </div>
                  <h2 className="value">189</h2>
                </div>
              </OverlayTrigger>
            </div>
            <div className="row justify-content-center">
              <div className="col full-width">
                <ul className="list-group-flush">
                  <li className="list-group-item">
                    <div className="concerns">
                      <h3>Health concerns from the contaminants over the legal limit:</h3>
                      <Table responsive borderless="true">
                        <tbody>
                          {legalLimitTableRows}
                        </tbody>
                      </Table>
                    </div>
                  </li>
                  <li className="list-group-item">
                    <div className="concerns">
                      <h3>Health concerns from the contaminants over the health guidelines:</h3>
                      <Table responsive borderless="true">
                        <tbody>
                          {healthGuidelinesTableRows}
                        </tbody>
                      </Table>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <button type="button" className="btn btn-secondary" onClick={hidePopup}>
            Close
          </button>
          <button type="button" className="btn btn-primary" onClick={showDetailView}>
            More Details
          </button>
        </Modal.Footer>
      </Modal>
    );
  }
}
Popup.propTypes = {
  showDetailView: PropTypes.func.isRequired,
  hidePopup: PropTypes.func.isRequired,
  countyID: PropTypes.string.isRequired,
  countyName: PropTypes.string.isRequired,
  stateID: PropTypes.string.isRequired,
};

export default Popup;
