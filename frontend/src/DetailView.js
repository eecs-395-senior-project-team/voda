import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Axios from 'axios';
import Log from './Log';
import './DetailView.sass';
import Tabs from 'react-bootstrap/Tabs';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Tab from 'react-bootstrap/Tab';
import ListGroup from 'react-bootstrap/ListGroup';
import Button from 'react-bootstrap/Button'; 
import Table from 'react-bootstrap/Table';

/**
 * DetailView Component.
 */
class DetailView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      details: '',
    };
  }

  componentWillMount() {
    const {countyID, stateID} = this.props;
    let apiURL;
    if (process.env.NODE_ENV === 'development') {
      apiURL = 'http://localhost:8000/'
    } else {
      apiURL = 'http://3.19.113.236:8000/'
    }
    const url = `${apiURL}details`
    Axios.get(url, {
      params: {
        source: `${stateID}${countyID}`,
      }
    })
      .then((details) => {
        this.setState({
          details: details.data,
        });
      })
      .catch((error) => {
        Log.error(error, 'Details Component');
      });
  }

  render() {
    const { details } = this.props;
    const { hideDetailView, countyName } = this.props;
    return (
      <div className="Details border border-dark rounded">
        <h1>Contaminant Details for {countyName} County</h1>
          <Tabs defaultActiveKey="profile" id="uncontrolled-tab-example">
            <Tab eventKey="home" title=<i className="fas fa-exclamation-triangle"></i>>
              <Tab.Container id="list-group-tabs-example" defaultActiveKey="#link1">
                <Row>
                  <Col sm={4}>
                    <ListGroup>
                      <ListGroup.Item action href="#link1">
                        Horrible Contaminent 1
                      </ListGroup.Item>
                      <ListGroup.Item action href="#link2">
                        Horrible Contaminent 2
                      </ListGroup.Item>
                    </ListGroup>
                  </Col>
                  <Col sm={8}>
                    <Tab.Content>
                      <Tab.Pane eventKey="#link1">
                        <div className = "Content">
                          <Table responsive borderless = 'true'>

                            <tbody>
                              <tr>
                                <td><h5><div className= "SmallHeader">Amount in water:</div></h5></td>
                                <td><h5><div className= "SmallHeader">Health Guideline:</div></h5></td>
                                <td><h5><div className= "SmallHeader">Legal Limit:</div></h5></td>
                              </tr>
                              <tr>
                                <td><div className="Numbers">7.38 *</div></td>
                                <td><div className="Numbers">0.06</div></td>
                                <td><div className="Numbers">999.99</div></td>
                              </tr>
                            </tbody>
                          </Table>
                          <p>
                          Bromodchloromecahne, one of the total TTHMs, is formed when chlorine or other disinfectants are used to treat
                                drinking water. Bromodchloromecahne and other disinfection byproducts inrease the risk of cancer and may cause problems during pregnancy.
                          </p>
                        </div>
                      </Tab.Pane>
                      <Tab.Pane eventKey="#link2">
                        <p>HI</p>
                      </Tab.Pane>
                    </Tab.Content>
                  </Col>
                </Row>
              </Tab.Container>

            </Tab>
            <Tab eventKey="profile" title= <i className="fas fa-notes-medical"></i>>

              <Tab.Container id="list-group-tabs-example" defaultActiveKey="#link1">
                <Row>
                  <Col sm={4}>
                    <ListGroup>
                      <ListGroup.Item action href="#link1">
                        Bad Contaminent 1
                      </ListGroup.Item>
                      <ListGroup.Item action href="#link2">
                        Bad Contaminent 2
                      </ListGroup.Item>
                    </ListGroup>
                  </Col>
                  <Col sm={8}>
                    <Tab.Content>
                      <Tab.Pane eventKey="#link1">
                        <div className = "Content">
                          <p>Amount in water:7.38 parts per billion <br /><br /> Health Guideline:0.06 parts per billion <br /><br />Legal Limit:999.99 parts per billion<br /><br /> 
                          Bromodchloromecahne, one of the total TTHMs, is formed when chlorine or other disinfectants are used to treat
                                drinking water. Bromodchloromecahne and other disinfection byproducts inrease the risk of cancer and may cause problems during pregnancy.
                          </p>
                        </div>
                      </Tab.Pane>
                      <Tab.Pane eventKey="#link2">
                        <p>HI</p>
                      </Tab.Pane>
                    </Tab.Content>
                  </Col>
                </Row>
              </Tab.Container>

            </Tab>
            <Tab eventKey="contact" title=<i className="fas fa-check"></i>>

              <Tab.Container id="list-group-tabs-example" defaultActiveKey="#link1">
                <Row>
                  <Col sm={4}>
                    <ListGroup>
                      <ListGroup.Item action href="#link1">
                        Good Contaminent 1
                      </ListGroup.Item>
                      <ListGroup.Item action href="#link2">
                        Good Contaminent 2
                      </ListGroup.Item>
                    </ListGroup>
                  </Col>
                  <Col sm={8}>
                    <Tab.Content>
                      <Tab.Pane eventKey="#link1">
                        <p>HI</p>
                      </Tab.Pane>
                      <Tab.Pane eventKey="#link2">
                        <p>HI</p>
                      </Tab.Pane>
                    </Tab.Content>
                  </Col>
                </Row>
              </Tab.Container>
            </Tab>
          </Tabs>
        <hr />
        <div className = "closeButton">
          <button type="button" className="btn btn-secondary" onClick={hideDetailView}>
            Close
          </button>
        </div>
     </div>
    );
  }
}

DetailView.propTypes = {
  hideDetailView: PropTypes.func.isRequired,
  countyID: PropTypes.string.isRequired,
  countyName: PropTypes.string.isRequired,
  stateID: PropTypes.string.isRequired,
};

export default DetailView;
