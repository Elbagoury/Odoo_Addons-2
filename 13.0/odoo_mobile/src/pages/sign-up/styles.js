import { StyleSheet, Dimensions, Platform } from 'react-native';

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
    width: undefined,
    justifyContent: 'center',
    marginTop: Platform.OS === 'ios' ? 20 : 0,
    backgroundColor: '#FFFFFF'
  },
  container: {
    marginLeft: 10,
    marginRight: 15
  },
  imageLogo: {
    width: Dimensions.get('window').width/2,
    alignSelf: 'center',
  },
  contentWrapper: {
    flex: 1,
    width: undefined,
    justifyContent: 'center',
  },
  formWrapper: {
    margin: 0,
  },
  loginHeader: {
    justifyContent: 'center',
    backgroundColor: "#000000",
    height: 40
  },
  loginHeaderLabel: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center'
  },
  inputText: {
    height: 50,
    paddingLeft: 0,
    color: '#000000'
  },
  inputTextArea: {
    height: 100,
    paddingLeft: 0,
    color: '#000000'
  },
  errorLabel: {
    color: '#FF0000',
    fontSize: 14,
    fontWeight: '600',
    textAlign: 'center',
    marginTop: 15,
    marginBottom: 5
  },
  buttonContainer: {
    marginTop: 15,
    marginLeft: 10,
  },
  loadingWrapper: {
    flex: 1,
    justifyContent: 'center',
    flexDirection: 'column',
    alignItems: 'center',
    alignSelf: 'center',
  },
  loading: {
    width: 64,
    height: 64
    // paddingTop: Dimensions.get('window').height/2,
  },
});

export default styles;