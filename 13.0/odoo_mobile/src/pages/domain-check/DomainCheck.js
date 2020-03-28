import React, { Component } from 'react';
import { View, Image, Keyboard, AsyncStorage, Modal, KeyboardAvoidingView } from 'react-native';
// import { Form, Item, Input, Text } from 'native-base';
import {
  Input,
  Layout,
} from "react-native-ui-kitten";
import Icon from 'react-native-vector-icons/FontAwesome';
import styles from './styles';
import Constants from '../../Constants';
import I18n from '../../i18n/i18n';
export default class DomainCheck extends Component {

  constructor(props) {
    super(props)
    const TAG = 'DOMAIN_CHECK';
    this.state = {
      domainName: '',
      session_id: '',
      domainNameError: false,
      loading: false,
      ranDomId: 0,
      showLogin: false,
    }
    this.checkDomainName = this.checkDomainName.bind(this);
    this.isLoading = this.isLoading.bind(this);
  }

  componentWillMount() {
    this.keyboardDidShowListener = Keyboard.addListener('keyboardDidShow', this._keyboardDidShow);
    this.keyboardDidHideListener = Keyboard.addListener('keyboardDidHide', this._keyboardDidHide);
  }

  componentWillUnmount() {
    this.keyboardDidShowListener.remove();
    this.keyboardDidHideListener.remove();
  }

  componentDidMount() {
    this.isLoading(false);
    AsyncStorage.getItem('company_domain').then(value => {
      if (value !== undefined) {
        this.setState({
          domainName: value,
        })
      }

      // if (this.state.domainName !== '' && this.state.domainName !== undefined && this.state.domainName !== null) {
      //   this.checkDomainName(this.state.domainName)
      // }
    });
  }

  _keyboardDidShow() {
    // alert('Keyboard Shown');
  }

  _keyboardDidHide() {
    // alert('Keyboard Hidden');
  }

  isLoading(isLoading) {
    this.setState({ loading: isLoading });
  }

  checkDomainName() {
    this.isLoading(true);
    Keyboard.dismiss()

    if (this.state.domainName !== '' && this.state.domainName !== undefined && this.state.domainName !== null) {
      this.setState({
        ranDomId: Math.floor(Math.random() * 1000) + 1,
        domainNameError: false,
        error: false,
      });

      let url = '';

      if (this.state.domainName.indexOf('odook8') > -1) {
        url = 'http://' + this.state.domainName + '/web/webclient/version_info';
      } else {
        url = 'https://' + this.state.domainName + '/web/webclient/version_info';
      }


      fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jsonrpc: "2.0",
          method: "call",
          params: {
            context: {}
          },
          id: 1234 + ''
        })
      })
        .then((response) => response.json())
        .then((responseJson) => {
          this.isLoading(false);
          if (responseJson.error) {
            this.setState({
              domainNameError: true,
              error: true
            })
            return;
          }

          console.log('abc');
          this.setState({
            domainNameError: false,
            error: false,
            // showLogin: true,
          });

          AsyncStorage.setItem('company_domain', this.state.domainName.toLowerCase().trim());
          this.props.navigation.navigate('Login_Page', {
            domainName: this.state.domainName.toLowerCase().trim()
          });
        })
        .catch((error) => {
          this.refs.domainInput._root.focus();
          this.isLoading(false)
          this.setState({
            domainNameError: true,
            error: true
          })
        })
    } else {
      this.refs.domainInput._root.focus();
      this.isLoading(false)
      this.setState({
        domainNameError: true,
        error: true
      })
    }
  }

  render() {
    return (
      <KeyboardAvoidingView style={styles.wrapper} behavior="padding">
        <View style={styles.wrapperContainer}>

          <Image source={require('../../../images/logo.png')}
            style={styles.imageLogo}
            resizeMode='contain' />

          <Input ref="domainInput"
            style={styles.input}
            size='small'
            placeholder={"Please input your domain"}
            value={this.state.domainName}
            onSubmitEditing={() => this.checkDomainName()}
            onChangeText={(domainName) => this.setState({ domainName })}
          />
        </View>
        {/* <Modal style={{flex: 1}} visible={this.state.showLogin}>
          <Text>Login here</Text>
        </Modal> */}
      </KeyboardAvoidingView>
    )
  }
}
