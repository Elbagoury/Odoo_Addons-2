import { Animated, Easing } from 'react-native';
import { createAppContainer } from "react-navigation";
import { createStackNavigator } from "react-navigation-stack";
import Home from './pages/home/Home'
import Authentication from './pages/authentication/Authentication'
import Login from './pages/login/Login'
import DomainCheck from './pages/domain-check/DomainCheck'
import SignUp from './pages/sign-up/SignUp'

const HomeStack = createStackNavigator({
  Authentication_Page: {
    screen: Authentication,
    navigationOptions: {
      header: null,
      gesturesEnabled: true,
    },
  },
  DomainCheck_Page: {
    screen: DomainCheck,
    navigationOptions: {
      header: null,
      gesturesEnabled: true,
    },
  },
  Login_Page: {
    screen: Login,
    navigationOptions: {
      header: null,
      gesturesEnabled: true,
    },
  },
  SignUp_Page: {
    screen: SignUp,
    navigationOptions: {
      header: null,
      gesturesEnabled: true,
    },
  },
  Home_Page: {
    screen: Home,
    navigationOptions: {
      header: null,
      gesturesEnabled: false,
    },
  },
}, {
    mode: 'modal',
    navigationOptions: {
      header: null,
    },
    transitionConfig: () => ({
      transitionSpec: {
        duration: 300,
        easing: Easing.out(Easing.poly(4)),
        timing: Animated.timing,
      },
      screenInterpolator: sceneProps => {
        const { layout, position, scene } = sceneProps;
        const { index } = scene;

        const height = layout.initHeight;
        const translateY = position.interpolate({
          inputRange: [index - 1, index, index + 1],
          outputRange: [height, 0, 0],
        });

        const opacity = position.interpolate({
          inputRange: [index - 1, index - 0.99, index],
          outputRange: [0, 1, 1],
        });

        return { opacity, transform: [{ translateY }] };
      },
    }),
  });

  export default createAppContainer(HomeStack);