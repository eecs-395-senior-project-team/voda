import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Link from '../Link.react';
import renderer from 'react-test-renderer';
import React from 'react';
import {render, fireEvent, cleanup} from 'react-testing-library';


// test that application launches without issues
it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div);
});


// test that popup opens without failure
// automatically unmount and cleanup DOM after the test is finished.
afterEach(cleanup);

it('showPopup displays after its clicked', () => {
  const {queryByLabelText, getByLabelText} = render(
    <App showPopup="On" showPopup="Off" />,
  );

  expect(queryByLabelText(/off/i)).toBeTruthy();

  fireEvent.click(getByLabelText(/off/i));

  expect(queryByLabelText(/on/i)).toBeTruthy();
});

// test that full view opens without failure
// automatically unmount and cleanup DOM after the test is finished.
afterEach(cleanup);

it('showPopup displays after its clicked', () => {
  const {queryByLabelText, showFullView} = render(
    <App showFullView="On" showPopup="Off" />,
  );

  expect(queryByLabelText(/off/i)).toBeTruthy();

  fireEvent.click(getByLabelText(/off/i));

  expect(queryByLabelText(/on/i)).toBeTruthy();
});