import React, { Component } from 'react';
import { View, WebView, Image, Keyboard, Platform, Modal } from 'react-native';
// import { Button, Text, Container, Content, Form, Item, Label, Input } from 'native-base';
import styles from './styles';

export default class SignUp extends Component {

  constructor(props) {
    super(props)
    const TAG = 'SIGN_UP'
    this.state = {
      domainName: this.props.navigation.state.params.domainName,
      name: '',
      email: '',
      phone: '',
      companyName: '',
      subject: '',
      message: '',
      error: false,
      behavior: 'padding',
      session_id: '',
      id: '',
      ranDomId: '',
      userNameError: false,
      passwordError: false,
      domainNameError: false,
      modalVisible: false,
      url: 'https://www.wcloud.vn/contactus',
      jsCode: `
        document.getElementsByTagName('header')[0].style.display = 'none';
        document.getElementsByClassName('contact-title')[0].style.display = 'none';
        document.getElementsByTagName('footer')[0].style.display = 'none';
      `,
    }
  }

  componentWillMount () {
    this.keyboardDidShowListener = Keyboard.addListener('keyboardDidShow', this._keyboardDidShow);
    this.keyboardDidHideListener = Keyboard.addListener('keyboardDidHide', this._keyboardDidHide);
  }

  componentWillUnmount () {
    this.keyboardDidShowListener.remove();
    this.keyboardDidHideListener.remove();
  }

  componentDidMount () {
    this.setModalVisible(false)
  }

  _keyboardDidShow () {
    // alert('Keyboard Shown');
  }

  _keyboardDidHide () {
    // alert('Keyboard Hidden');
  }

  setModalVisible(visible) {
    this.setState({modalVisible: visible});
  }

  onNavigationStateChange(navState) {
    // let domain = ''
    if (navState.url.indexOf('contactus-thank-you') > -1) {
      // go to success page
      this.setState({
        modalVisible: true,
      });
    }
  }

  onLoadEnd() {

  }

  goBack() {
    this.setState({
      modalVisible: false,
    });
    this.props.navigation.navigate('Authentication_Page', {});
  }

  // signUp() {
  //   this.setState({
  //     url: 'https://www.wcloud.vn/contactus',
  //   });
  //   // console.log(this.state);
  // }

  render() {
    return (
      <View style={styles.wrapper}>
        <WebView
          source={{uri: this.state.url}}
          onNavigationStateChange={this.onNavigationStateChange.bind(this)}
          onLoadEnd={this.onLoadEnd.bind(this)}
          startInLoadingState={true}
          injectedJavaScript={this.state.jsCode}
          style={{
            marginTop: Platform.OS === 'ios' ? 20 : 0
        }}/>
        {/* <Container style={styles.wrapper}>

            <Content style={styles.container}>
                <Image source={require('../../../images/w360s-logo.jpg')}
                    style={styles.imageLogo}
                    resizeMode='contain'
                  />
                <Form style={styles.formWrapper}>
                  <Item stackedLabel error={this.state.userNameError} style={styles.inputTextWrapper}>
                      <Label>Name</Label>
                      <Input autoCapitalize={'none'} style={styles.inputText}
                          autoCorrect={false}
                          onChangeText={(name) => this.setState({name})}
                          value={this.state.name}/>
                  </Item>
                  <Item stackedLabel error={this.state.passwordError} style={styles.inputTextWrapper}>
                      <Label>Email</Label>
                      <Input autoCapitalize={'none'} style={styles.inputText}
                          onChangeText={(email) => this.setState({email})}
                          value={this.state.email}/>
                  </Item>
                  <Item stackedLabel error={this.state.userNameError} style={styles.inputTextWrapper}>
                      <Label>Phone number</Label>
                      <Input autoCapitalize={'none'} style={styles.inputText}
                          autoCorrect={false}
                          onChangeText={(phone) => this.setState({phone})}
                          value={this.state.phone}/>
                  </Item>
                  <Item stackedLabel error={this.state.userNameError} style={styles.inputTextWrapper}>
                      <Label>Company name</Label>
                      <Input autoCapitalize={'none'} style={styles.inputText}
                          autoCorrect={false}
                          onChangeText={(companyName) => this.setState({companyName})}
                          value={this.state.companyName}/>
                  </Item>
                  <Item stackedLabel error={this.state.userNameError} style={styles.inputTextWrapper}>
                      <Label>Subject</Label>
                      <Input autoCapitalize={'none'} style={styles.inputText}
                          autoCorrect={false}
                          onChangeText={(subject) => this.setState({subject})}
                          value={this.state.subject}/>
                  </Item>
                  <Item stackedLabel error={this.state.userNameError} style={styles.inputTextWrapper}>
                      <Label>Message</Label>
                      <Input autoCapitalize={'none'} multiline={true} numberOfLines={10} style={styles.inputTextArea}
                          autoCorrect={false}
                          onChangeText={(message) => this.setState({message})}
                          value={this.state.message}/>
                  </Item>
                  {this.state.error && <Text style={styles.errorLabel}>Please check your login info</Text>}
                  <Button full success style={styles.buttonContainer}
                      onPress={() => this.signUp()}>
                      <Text>SIGN UP</Text>
                  </Button>
                </Form>
            </Content>
        </Container> */}
        {/* <Modal animationType="fade"
          transparent={false}
          visible={this.state.modalVisible}>
          <View style={styles.loadingWrapper}>
            <Image source={require('../../../images/ic_check_mark_done.png')}
              style={styles.loading}
              resizeMode='contain'/>
            <Text>Your request was successfully submitted to our system.</Text>
            <Text>An email will send to you or our support team will contact you for more information.</Text>
            <Text>Thank you!</Text>
            <Button full success style={styles.buttonContainer} onPress={() => this.goBack()}>
              <Text>Back To Main Screen</Text>
            </Button>
          </View>
        </Modal> */}
      </View>
    );
  }
}

