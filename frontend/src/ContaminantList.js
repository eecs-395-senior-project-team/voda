import React from 'react';
import PropTypes from 'prop-types';
import Nav from 'react-bootstrap/Nav';
import './ContaminantList.sass';

/**
 * ContaminantList component
 */
function ContaminantList({ contaminants, setCurrentContaminant }) {
  const listItems = [];
  for (let i = 0; i < contaminants.length; i += 1) {
    listItems.push(
      <Nav.Item key={`navkey-${i}`}>
        <Nav.Link
          eventKey={`#item${i}`}
          onSelect={setCurrentContaminant}
          className="navigation-item"
        >
          {contaminants[i]}
        </Nav.Link>
      </Nav.Item>,
    );
  }
  return (
    <Nav variant="pills" className="flex-column" defaultActiveKey="#item0">
      {listItems}
    </Nav>
  );
}
ContaminantList.propTypes = {
  contaminants: PropTypes.arrayOf(String).isRequired,
  setCurrentContaminant: PropTypes.func.isRequired,
};

export default ContaminantList;
