import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Axios from 'axios';
import Modal from 'react-bootstrap/Modal';
import Log from './Log';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger'; // maybe keep
import Tooltip from 'react-bootstrap/Tooltip'; // probs keep
import Button from 'react-bootstrap/Button'; // probs keep?
import Table from 'react-bootstrap/Table';
import './Popup.sass';

/**
 * Popup card component.
 */
class Popup extends Component {
  constructor(props) {
    super(props);
    this.state = {
      summary: '',
    };
  }

  componentWillMount() {
    const { countyID, stateID } = this.props;
    let apiURL;
    if (process.env.NODE_ENV === 'development') {
      apiURL = 'http://localhost:8000/'
    } else {
      apiURL = 'http://3.19.113.236:8000/'
    }
    const url = `${apiURL}summary`
    Log.info(url)
    Axios.get(url, {
      params: {
        source: `${stateID}${countyID}`,
      }
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
    const { summary } = this.state;
    const {
      showDetailView,
      hidePopup,
      countyName, } = this.props;
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
        <Modal.Body
          dialogClassName="body"
        >
          <div className="container-fluid">
            <div className="row justify-content-center">
              <OverlayTrigger
                overlay={
                  <Tooltip id="tooltip">
                    Number of contaminants above the legal limit
                  </Tooltip>
                }
                placement='top'
              >
                <div className="col-sm-4 bg-danger">
                  <div>
                    <h2><i className="fas fa-exclamation-triangle"></i></h2>
                  </div>
                  <h2 className="value">3</h2>
                </div>
              </OverlayTrigger>
              <OverlayTrigger
                overlay={
                  <Tooltip id="tooltip">
                    Number of contaminants above the health guideline
                  </Tooltip>
                }
                placement='top'
              >
                <div className="col-sm-4 bg-warning">
                    <div>
                      <h2><i className="fas fa-notes-medical"></i></h2>
                    </div>
                    <h2 className="value">8</h2>
                </div> 
              </OverlayTrigger>
              <OverlayTrigger
                overlay={
                  <Tooltip id="tooltip">
                    Number of contaminants that meet the health guideline
                  </Tooltip>
                }
                placement='top'
                >
                  <div className="col-sm-4 bg-success">
                    <div>
                      <h2><i className="fas fa-check"></i></h2>
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
                      <Table responsive borderless = 'true'>

<tbody>
  <tr>
    <td>Cancer</td>
    <td>Change in blood pressure</td>
    <td>Filler condition</td>
  </tr>
  <tr>
    <td>Another filler condition</td>
    <td>Harm to the adrenal gland</td>
    <td>filler condition</td>
  </tr>
</tbody>
</Table>

                    </div>
                  </li>
                  <li className="list-group-item">
                    <div className="concerns">
                      <h3>Health concerns from the contaminants over the health guidelines:</h3>
                      <p> Harm to the central nervous system, Harm to the adrenal gland, Change to blood cells</p>
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
