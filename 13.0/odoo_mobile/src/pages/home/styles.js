import { StyleSheet, Platform } from 'react-native';

const styles = StyleSheet.create({
  // paddingTop: Platform.OS === 'ios' ? 35 : 0,
  container: {
    marginTop: Platform.OS === 'ios' ? 35 : 0,
    flex: 1
  },
  loading: { position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center', backgroundColor: '#FFFFFF' }
});

export default styles;