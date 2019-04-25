import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Axios from 'axios';
import Modal from 'react-bootstrap/Modal';
import './Popup.sass';
import './PopupStyle.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'
import { faNotesMedical } from '@fortawesome/free-solid-svg-icons'
import { faCheck } from '@fortawesome/free-solid-svg-icons'

library.add(faExclamationTriangle)
library.add(faNotesMedical)
library.add(faCheck)

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
  }



  render() {
    const { summary } = this.state;
    const { hidePopup, countyName } = this.props;
    
    return (
      <Modal
        show
        onHide={hidePopup}
        dialogClassName="popup"
      >
        <Modal.Header closeButton>
          <Modal.Title >
            {`Contaminant Summary For ${countyName} County`}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div class="container">
              <div class="row justify-content-center features">
                  <div class="col-sm-6 col-md-5 col-lg-4 item bg-danger">
                      <div class="box">
                        <h2><FontAwesomeIcon icon="exclamation-triangle" /></h2>
                      </div>
                      <h2 class="value">3</h2>
                  </div>
                  <div class="col-sm-6 col-md-5 col-lg-4 item bg-warning">
                      <div class="box">
                        <h2><FontAwesomeIcon icon="notes-medical" /></h2>
                      </div>
                      <h2 class="value">8</h2>
                  </div>
                  <div class="col-sm-6 col-md-5 col-lg-4 item bg-success">
                      <div class="box">
                          <h2><FontAwesomeIcon icon="check" /></h2>

                          <h2 class="value">189 </h2>
                      </div>
                  </div>
              </div>
          </div>
          <ul class="list-group">
              <li class="list-group-item">
                  <div class="concerns">
                      <p>Health concerns from the contaminants over the legal limit: cancer, change in blood pressure</p>
                  </div>
              </li>
              <li class="list-group-item">
                  <div class="concerns">
                      <p>Health concerns from the contaminants over the health guidelines: Harm to the central nervous system, Harm to the adrenal gland, Change to blood cells</p>
                  </div>
              </li>
          </ul>
        </Modal.Body>
        <Modal.Footer>
          <button type="button" className="btn btn-secondary" onClick={hidePopup}>
            Close
          </button>
          <button type="button" class="btn btn-secondary" data-toggle="tooltip" data-placement="top" title="Tooltip on top">
  Tooltip on top
          </button>
          <button type="button" className="btn btn-primary">
            More Details
          </button>
        </Modal.Footer>
      </Modal>
    );
  }
}
Popup.propTypes = {
  hidePopup: PropTypes.func.isRequired,
  countyID: PropTypes.string.isRequired,
  countyName: PropTypes.string.isRequired,
  stateID: PropTypes.string.isRequired,
};

export default Popup;
