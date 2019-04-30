import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Axios from 'axios';
import Modal from 'react-bootstrap/Modal';
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
    const { summary } = this.state;
    const {
      showDetailView,
      hidePopup,
      countyName,
    } = this.props;
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
              <div className="col-sm-4 bg-danger">
                <div>
                  <h2><i className="fas fa-exclamation-triangle" /></h2>
                </div>
                <h2 className="value">3</h2>
              </div>
              <div className="col-sm-4 bg-warning">
                <div>
                  <h2><i className="fas fa-notes-medical" /></h2>
                </div>
                <h2 className="value">8</h2>
              </div>
              <div className="col-sm-4 bg-success">
                <div>
                  <h2><i className="fas fa-check" /></h2>
                </div>
                <h2 className="value">189</h2>
              </div>
            </div>
            <div className="row justify-content-center">
              <div className="col full-width">
                <ul className="list-group">
                  <li className="list-group-item">
                    <div className="concerns">
                      <p>Health concerns from the contaminants over the legal limit: cancer, change in blood pressure</p>
                    </div>
                  </li>
                  <li className="list-group-item">
                    <div className="concerns">
                      <p>Health concerns from the contaminants over the health guidelines: Harm to the central nervous system, Harm to the adrenal gland, Change to blood cells</p>
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
