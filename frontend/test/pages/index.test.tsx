import React from 'react';
import { default as Home } from '../../pages/index';
import { render } from '../testUtils';

describe('Home page', () => {
  it('matches snapshot', () => {
    const { asFragment } = render(<Home />, {});
    expect(asFragment()).toMatchSnapshot();
  });
});
