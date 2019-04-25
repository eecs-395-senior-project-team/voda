import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Axios from 'axios';
import Modal from 'react-bootstrap/Modal';
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
  }

  render() {
    const { summary } = this.state;
    const { hidePopup, showDetail, countyName} = this.props;
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
          <p className="lead">{summary}</p>
        </Modal.Body>
        <Modal.Footer>
          <button type="button" className="btn btn-secondary" onClick={hidePopup}>
            Close
          </button>
          <button type="button" className="btn btn-primary" onClick = {showDetail}>
            More Details
          </button>
        </Modal.Footer>
      </Modal>
    );
  }
}

Popup.propTypes = {
  hidePopup: PropTypes.func.isRequired,
  showDetail: PropTypes.func.isRequired,
  countyID: PropTypes.string.isRequired,
  countyName: PropTypes.string.isRequired,
  stateID: PropTypes.string.isRequired,
};

export default Popup;
