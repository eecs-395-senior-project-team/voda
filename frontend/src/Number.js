import React from 'react';
import PropTypes from 'prop-types';
import "./Number.sass";

/**
 * Number component
 */
function Number({ value }) {
  let num;
  if (value) {
    num = (
      <div className="Numbers">
        {value}
        <span className="unit"> ppb</span>
      </div>
    );
  } else {
    num = (
      <div className="Numbers">
        N/A
        <sup>*</sup>
      </div>
    );
  }
  return num;
}
Number.propTypes = {
  value: PropTypes.number,
};

export default Number;
