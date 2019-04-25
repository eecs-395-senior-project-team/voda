import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Axios from 'axios';
import Modal from 'react-bootstrap/Modal';
import './Detail.sass';


/**
 * Popup card component.
 */
class Detail extends Component {
  constructor(props) {
    super(props);
    this.state = {
      detail: '',
    };
  }

  componentWillMount() {
    const { countyID, stateID } = this.props;
  }

  render() {
    const { detail } = this.state;
    const { hideDetail, countyName } = this.props;
    return (
      <Modal
        show = {this.state.show}
        onHide={hideDetail}
        dialogClassName="detail"
      >
        <Modal.Header closeButton>
          <Modal.Title>
            {`Contaminant DETAILS For ${countyName} County`}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="lead">{detail}</p>
        </Modal.Body>
        <Modal.Footer>
          <button type="button" className="btn btn-secondary" onClick={hideDetail}>
            Close
          </button>
        </Modal.Footer>
      </Modal>
    );
  }
}
Detail.propTypes = {
  hideDetail: PropTypes.func.isRequired,
  countyID: PropTypes.string.isRequired,
  countyName: PropTypes.string.isRequired,
  stateID: PropTypes.string.isRequired,
};

export default Detail;
