import React, { Component } from 'react';
import { mapping, light as lightTheme } from '@eva-design/eva';
import HomeStack from './Router';
import { ApplicationProvider } from 'react-native-ui-kitten';

console.disableYellowBox = true;

export default class App extends Component {
  render() {
    return <ApplicationProvider mapping={mapping} theme={lightTheme}>
      <HomeStack />
    </ApplicationProvider>
  }
}
