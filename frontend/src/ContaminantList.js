import React from 'react';
import PropTypes from 'prop-types';
import './ContaminantList.sass';
import Nav from 'react-bootstrap/Nav';

/**
 * ContaminantList component
 */
function ContaminantList({ contaminants }) {
  const listItems = [];
  for (let i = 0; i < contaminants.length; i += 1) {
    listItems.push(
      <Nav.Item key={`navkey-${i}`}>
        <Nav.Link eventKey={`#item${i}`}>
          {contaminants[i]}
        </Nav.Link>
      </Nav.Item>,
    );
  }
  return (
    <Nav variant="pills" className="Contaminant-list flex-column">
      {listItems}
    </Nav>
  );
}
ContaminantList.propTypes = {
  contaminants: PropTypes.arrayOf(String).isRequired,
};

export default ContaminantList;
