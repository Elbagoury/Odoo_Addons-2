import React, { Component } from 'react';
import { View, Image, Keyboard, AsyncStorage, KeyboardAvoidingView, Alert, Text } from 'react-native';
import {
  Input,
  Button,
  Layout,
} from "react-native-ui-kitten";
// import { Container, Content, Form, Item, Input, Label, Button, Text } from 'native-base';
import styles from './styles';
// import Spinner from 'react-native-loading-spinner-overlay';
import I18n from '../../i18n/i18n';
export default class Login extends Component {

  constructor(props) {
    super(props)
    const TAG = 'LOGIN'
    this.state = {
      domainName: this.props.navigation.state.params.domainName,
      username: '',
      password: '',
      databaseName: '',
      error: false,
      behavior: 'padding',
      session_id: '',
      id: '',
      ranDomId: '',
      userNameError: false,
      passwordError: false,
      domainNameError: false,
      loading: false,
      isDbNotCorrect: false,
    }
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
    this.isLoading(false)

    AsyncStorage.multiGet(['username', 'password']).then(values => {
      // console.log(values)
      if (values !== null && values !== undefined) {
        this.setState({
          username: values[0][1],
          password: values[1][1]
        })
      }
      // if (this.checkInfo(this.state.username) && this.checkInfo(this.state.password)) {
      //   this.login()
      // }
    });
  }

  checkInfo(info) {
    if (info !== null && info !== '' && info !== undefined) {
      return true
    } else {
      return false
    }
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

  login = () => {
    this.isLoading(true)
    Keyboard.dismiss()
    // let db = this.state.username.substring(this.state.username.lastIndexOf("@") + 1)
    if (this.state.userNameError || this.state.passwordError) {
      this.isLoading(false)
    } else {
      let db = '';
      if (this.state.isDbNotCorrect) {
        db = this.state.databaseName;
      } else {
        if (this.state.domainName.indexOf('www') > -1) {
          db = this.state.domainName.substring(this.state.domainName.indexOf('.') + 1);
        } else {
          db = this.state.domainName;
        }
      }

      this.setState({ ranDomId: Math.floor(Math.random() * 1000) + 1 })

      let url = '';

      if (this.state.domainName.indexOf('odook8') > -1) {
        db = 'odoo';
        url = 'http://' + this.state.domainName + '/web/session/authenticate';
      } else {
        url = 'https://' + this.state.domainName + '/web/session/authenticate';
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
            db: db,
            login: this.state.username,
            password: this.state.password,
            context: {}
          },
          id: 1234 + ''
        })
      })
        .then(response => response.json())
        .then((responseJson) => {
          this.isLoading(false);
          // console.log(responseJson);
          if (responseJson.error) {
            this.setState({
              error: true
            });
            if (responseJson.error.data.message.indexOf('database') > -1 && responseJson.error.data.message.indexOf('does not exist') > -1) {
              console.log('incorrect database');
              this.setState({
                isDbNotCorrect: true
              });
            } else {
              this.setState({
                isDbNotCorrect: false
              });
            }
            return;
          }
          // Alert.alert("debug", JSON.stringify(responseJson));
          this.setState({
            session_id: responseJson.result.session_id
          });
          AsyncStorage.setItem('username', this.state.username.toLowerCase().trim())
          AsyncStorage.setItem('password', this.state.password)
          this.props.navigation.navigate('Home_Page', {
            domainName: this.state.domainName.toLowerCase().trim(),
            username: this.state.username.toLowerCase().trim(),
            password: this.state.password,
            session_id: this.state.session_id
          });
        })
        .catch((error) => {
          // console.error(error)
          this.isLoading(false)
          this.setState({
            error: true
          })
        });
    }
  }

  render() {
    return (
      <KeyboardAvoidingView style={styles.wrapper} behavior="padding">

        <Layout style={styles.wrapperContainer}>

          <Image source={require('../../../images/w360s-logo.jpg')}
            style={styles.imageLogo}
            resizeMode='contain'
          />
          <Input autoCapitalize={'none'} style={styles.inputText}
            autoCorrect={false} size='small' placeholder={"Username"}
            onChangeText={(username) => this.setState({ username })}
            value={this.state.username} />
          <Input secureTextEntry={true} style={styles.inputText}
            size='small' placeholder={"Password"}
            onChangeText={(password) => this.setState({ password })}
            value={this.state.password} />
          {this.state.isDbNotCorrect && <View stackedLabel error={this.state.databaseError} style={styles.inputTextWrapper}>
            {/* <Label>{I18n.t('lbl_database_name')}</Label> */}
            <Input autoCapitalize={'none'} autoCorrect={false} style={styles.inputText}
              size='small' placeholder={"Database Name"}
              onChangeText={(databaseName) => this.setState({ databaseName })}
              value={this.state.databaseName} />
          </View>}

          {this.state.error && !this.state.isDbNotCorrect && <Text style={styles.errorLabel}>{I18n.t('lbl_err_msg_0001')}</Text>}
          {this.state.error && this.state.isDbNotCorrect && <Text style={styles.errorLabel}>
            {I18n.t('lbl_err_msg_0005')}
          </Text>}

          <Button status="success" style={styles.buttonContainer} onPress={() => this.login()}>
            {I18n.t('lbl_login')}
          </Button>
        </Layout>
      </KeyboardAvoidingView>
    );
  }
}
