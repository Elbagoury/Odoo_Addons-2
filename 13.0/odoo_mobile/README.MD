react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res/

$ cd android
#Create debug build:
$ ./gradlew assembleDebug
#Create release build:
$ ./gradlew assembleRelease


#Patch port
`rnp patch -o 8081 -n 8899`