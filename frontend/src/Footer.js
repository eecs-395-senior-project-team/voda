import React from 'react';
import PropTypes from 'prop-types';
import './Footer.css';

/**
 * Footer component
 */
function Footer({ footer }) {
  return (
    <div className="row">
      <div className="col">
        <div className="Footer">
          <footer>
            {footer}
          </footer>
        </div>
      </div>
    </div>
  );
}
Footer.propTypes = {
  footer: PropTypes.string.isRequired,
};

export default Footer;
