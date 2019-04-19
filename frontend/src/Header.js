import React from 'react';
import PropTypes from 'prop-types';
import './Header.sass';

/**
 * Header component
 */
function Header({ header }) {
  return (
    <div className="row justify-content-between">
      <div className="col-xs-4">
        <div className="Header text-uppercase">
          <header>
            <h1>
              {header}
            </h1>
          </header>
        </div>
      </div>
      <div className="col-xs-4">
        <div className="github">
          <a href="https://github.com/eecs-395-senior-project-team/voda">
            <i className="fab fa-github fa-2x" />
          </a>
        </div>
      </div>
    </div>
  );
}
Header.propTypes = {
  header: PropTypes.string.isRequired,
};

export default Header;
