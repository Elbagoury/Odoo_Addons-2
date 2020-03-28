import React, { Component } from 'react'
import { Platform, AsyncStorage, ActivityIndicator, View } from 'react-native';
import { WebView } from 'react-native-webview';
import styles from './styles';

export default class Home extends Component {

  constructor(props) {
    super(props)
    this.state = {
      url: 'about:blank',
      username: this.props.navigation.state.params.username,
      password: this.props.navigation.state.params.password,
      company_domain: '',
      session_id: this.props.navigation.state.params.session_id,
      jsCode: '',
      isInjectedJS: false,
      isLoggedIn: false,
      isLoggedOut: false,
    }
  }

  componentWillMount() {
    this.setState({
      jsCode: `setTimeout(() => {
        if (document.getElementsByName('login')[0]) {
          document.getElementsByName('login')[0].value = '${this.state.username}';
          document.getElementsByName('password')[0].value = '${this.state.password}';
          var index = -1;
          for (var i=0; i<document.getElementsByTagName('button').length; i++) {
            if (document.getElementsByTagName('button')[i].type === 'submit') {
              index = i;
            }
          }
          if (index === -1) {

          } else {
            document.getElementsByTagName('button')[index].click();
          }
        }
      }, 500);`,
    });
  }

  componentDidMount() {
    this.setState({
      url: 'http://' + this.props.navigation.state.params.domainName + '/web#home',
    });

    AsyncStorage.getItem('username').then(value => {
      if (value !== undefined) {
        this.setState({
          username: value,
        })
      }
    });

    AsyncStorage.getItem('password').then(value => {
      if (value !== undefined) {
        this.setState({
          password: value,
        })
      }
    });

    AsyncStorage.getItem('company_domain').then(value => {
      if (value !== undefined) {
        this.setState({
          company_domain: value,
        })
      }
    });
  }

  componentWillUnmount() {
    this.setState({
      isLoggedIn: false
    });
  }

  loadEnd = () => {
    setTimeout(() => {
      if (!this.state.isInjectedJS) {
        this.setState({
          isInjectedJS: true
        }, () => {
          this.webref.injectJavaScript(this.state.jsCode);
          setTimeout(() => {
            this.setState({
              isLoggedIn: true
            });
          }, 3500);
        });
      }
    }, 1500);
  }

  onNavigationStateChange = (navState) => {
    // console.log(navState.url);
    let domain = '';
    if (this.props.navigation.state.params.domainName.indexOf('odook8') > -1) {
      domain = 'http://' + this.props.navigation.state.params.domainName + '/web';
    } else {
      domain = 'https://' + this.props.navigation.state.params.domainName + '/web';
    }
    if (navState.url.indexOf('logout') > -1) {
      this.backToLogin();
      this.setState({ url: '' })
    } else if (navState.url == (domain + '/login#home')) {
      navState.url = domain + '#home';
      this.setState({
        url: domain + '#home',
      });
    }

    if (navState.url === 'https://' + this.props.navigation.state.params.domainName + '/web/login') {
      this.backToLogin();
      this.setState({ url: '' })
    }
  }

  backToLogin = () => {
    if (!this.state.isLoggedOut) {
      this.setState({
        isLoggedOut: true,
      });
      AsyncStorage.setItem('company_domain', '')
      AsyncStorage.setItem('username', '')
      AsyncStorage.setItem('password', '')
      this.props.navigation.navigate('Authentication_Page', {});
    }
  }

  render() {
    return (
      <View style={styles.container}>
        <WebView ref={r => (this.webref = r)}
          source={{ uri: this.state.url }}
          onNavigationStateChange={this.onNavigationStateChange}
          startInLoadingState={true}
          onLoadEnd={this.loadEnd}
          javaScriptEnabled={true}
          allowFileAccess={true}
        />
        {!this.state.isLoggedIn && <View style={styles.loading}>
          <ActivityIndicator size="large" />
        </View>}
      </View>
    )
  }
}
