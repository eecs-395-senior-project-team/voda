import React from 'react';
import PropTypes from 'prop-types';

/**
 * Number component
 */
function Number({ value }) {
  let num;
  if (value) {
    num = (
      <div>
        {value}
        <span className="unit"> ppb</span>
      </div>
    );
  } else {
    num = (
      <div>
        N/A<sup>*</sup>
      </div>
    )
  }
  return num;
}
Number.propTypes = {
  value: PropTypes.number.isRequired,
};

export default Number;
