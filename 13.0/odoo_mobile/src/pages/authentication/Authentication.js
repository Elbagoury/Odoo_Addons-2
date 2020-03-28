import React, { Component } from 'react';
import { View, Image, Keyboard, Modal, KeyboardAvoidingView, Text, TouchableOpacity } from 'react-native';
// import { Form, Button, Text } from 'native-base';
import {
  Button,
  Layout,
} from 'react-native-ui-kitten';
import styles from './styles';
import I18n from "../../i18n/i18n";
export default class Authentication extends Component {

  constructor(props) {
    super(props)
    const TAG = 'AUTHENTICATION'
    this.state = {
      domainName: '',
      session_id: '',
      domainNameError: false,
      ranDomId: 0,
      loading: false,
      isEnabledSignUp: false,
    }
  }

  componentWillMount() {
    this.keyboardDidShowListener = Keyboard.addListener('keyboardDidShow', this._keyboardDidShow);
    this.keyboardDidHideListener = Keyboard.addListener('keyboardDidHide', this._keyboardDidHide);

    // fetch('https://raw.githubusercontent.com/boomlord/wcloud-configuration/master/db.json', {
    //   method: 'GET',
    //   headers: {
    //     'Accept': 'application/json',
    //     'Content-Type': 'application/json',
    //     'Cache-Control': 'no-cache',
    //   },
    // })
    // .then(response => response.json())
    // .then((responseJson) => {
    //   console.log(responseJson);
    //   this.setState({
    //     isEnabledSignUp: responseJson.signUp.isEnabled,
    //   })
    // })
    // .catch((error) => {
    //   // console.error(error);
    // });
  }

  componentWillUnmount() {
    this.keyboardDidShowListener.remove();
    this.keyboardDidHideListener.remove();
  }

  componentDidMount() {

  }

  _keyboardDidShow() {
    // alert('Keyboard Shown');
  }

  _keyboardDidHide() {
    // alert('Keyboard Hidden');
  }

  login() {
    this.props.navigation.navigate('DomainCheck_Page', {});
  }

  signUp() {
    this.props.navigation.navigate('SignUp_Page', {});
  }
  render() {
    return (
      <KeyboardAvoidingView style={styles.wrapper} behavior="padding">
        <Layout style={styles.wrapperContainer}>
          <Image source={require('../../../images/logo.png')}
            style={styles.imageLogo}
            resizeMode='contain' />

          <Button status="success" onPress={() => this.login()} style={styles.formBtn}>
            {I18n.t('lbl_login')}
          </Button>

          {/* <Form style={styles.formWrapper}>
            <Button block success onPress={() => this.login()} style={styles.formBtn}>
              <Text>{I18n.t('lbl_login')}</Text>
            </Button>
            {this.state.isEnabledSignUp && <Button block success onPress={() => this.signUp()} style={styles.formBtn}>
              <Text>{I18n.t('lbl_signup')}</Text>
            </Button>}
          </Form> */}
        </Layout>
      </KeyboardAvoidingView>
    )
  }
}
