import React, { Component } from 'react';
import PropTypes from 'prop-types';
import './TabDetails.sass';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import TabContainer from 'react-bootstrap/TabContainer';
import TabContent from 'react-bootstrap/TabContent';
import TabPane from 'react-bootstrap/TabPane';
import Table from 'react-bootstrap/Table';
import ContaminantList from './ContaminantList';

/**
 * A set of tab components for a Detail View
 */
class TabDetails extends Component {
  constructor(props) {
    super(props);
    this.state = {
      contaminantDetails: [],
    };
  }

  render() {
    const {
      contaminants,
    } = this.props;
    const tabPanes = [];
    for (let i = 0; i < contaminants.length; i += 1) {
      tabPanes.push(
        <TabPane
          key={`#pane-key-${i}`}
          eventKey={`#item${i}`}
        >
          <div className="pane-body">
            <Table responsive borderless="true">
              <tbody>
                <tr>
                  <td>
                    <h5>
                      <div className="SmallHeader">
                        Amount in water:
                      </div>
                    </h5>
                  </td>
                  <td>
                    <h5>
                      <div className="SmallHeader">
                        Health Guideline:
                      </div>
                    </h5>
                  </td>
                  <td>
                    <h5>
                      <div className="SmallHeader">
                        Legal Limit:
                      </div>
                    </h5>
                  </td>
                </tr>
                <tr>
                  <td>
                    <div className="Numbers">
                      7.38
                      <span className="unit"> ppb</span>
                    </div>
                  </td>
                  <td>
                    <div className="Numbers">
                      0.06
                      <span className="unit"> ppb</span>
                    </div>
                  </td>
                  <td>
                    <div className="Numbers">
                      999.99
                      <span className="unit"> ppb</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </Table>
            <p>
              Bromodchloromecahne, one of the total TTHMs, is formed when chlorine or other disinfectants are used to treat
                    drinking water. Bromodchloromecahne and other disinfection byproducts inrease the risk of cancer and may cause problems during pregnancy.
            </p>
          </div>
        </TabPane>,
      );
    }
    return (
      <TabContainer defaultActiveKey="#item0">
        <Row>
          <Col sm={4}>
            <ContaminantList contaminants={contaminants} />
          </Col>
          <Col sm={8}>
            <TabContent>
              {tabPanes}
            </TabContent>
          </Col>
        </Row>
      </TabContainer>
    );
  }
}
TabDetails.propTypes = {
  contaminants: PropTypes.arrayOf(String).isRequired,
  countyID: PropTypes.string.isRequired,
  stateID: PropTypes.string.isRequired,
};

export default TabDetails;
