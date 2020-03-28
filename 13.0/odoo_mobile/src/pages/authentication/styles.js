import { StyleSheet, Dimensions, Platform } from 'react-native';

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
    justifyContent: 'center',
    paddingTop: Platform.OS === 'ios' ? 20 : 0,
    flexDirection: 'column',
    alignItems: 'center',
    backgroundColor: '#FFFFFF'
  },
  wrapperContainer: {
    // backgroundColor: '#FF0000',
    height: Dimensions.get('window').height / 2,
  },
  formWrapper: {
    justifyContent: 'center',
    alignItems: 'center',
    width: Dimensions.get('window').width,
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-around'
  },
  formBtn: {

  },
  imageLogo: {
    width: Dimensions.get('window').width / 2,
    alignSelf: 'center',
    marginBottom: 100
  },
  inputTextWrapper: {
    marginRight: 15,
  },
  inputText: {
    height: 40,
    color: '#000000',
    backgroundColor: '#ebebeb',
    textAlign: 'center',
  },
  nextBtn: {
    color: 'black',
    fontSize: 16,
    fontWeight: "300",
    position: 'absolute',
    right: 0,
    marginRight: 10,
  },
  errorLabel: {
    color: '#FF0000',
    fontSize: 14,
    fontWeight: '600',
    textAlign: 'center',
    marginTop: 15,
    marginBottom: 5,
    width: Dimensions.get('window').width - 10,
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
    height: 64,
    // paddingTop: Dimensions.get('window').height/2,
  },
  spinnerTextStyle: {
    color: '#FFF'
  },
});

export default styles;
