import React from 'react';
import PropTypes from 'prop-types';
import './Header.css';

/**
 * Header component
 */
function Header({ header }) {
  return (
    <div className="row">
      <div className="col-xs-12">
        <div className="Header text-uppercase">
          <header>
            <h1>
              {header}
            </h1>
          </header>
        </div>
      </div>
    </div>
  );
}
Header.propTypes = {
  header: PropTypes.string.isRequired,
};

export default Header;
