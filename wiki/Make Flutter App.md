---
tags: ['#ref', '#wip']
---

已經用於 [[Custom Headache App]] ，能夠製作包含資料庫的簡單介面

reference

- [頭痛app * Google 雲端硬碟](https://drive.google.com/drive/folders/1NQdaI7wGIeh_rP99JFQnXUlaEvkE24xL)

- install : https://docs.flutter.dev/get-started/install/windows
	- android 5.0 : `C:\Users\User\AppData\Local\Android\Sdk\tools\bin\sdkmanager.bat --install "cmdline-tools;latest"`
	- `flutter doctor --android-licenses`
	- [Test drive Flutter](https://docs.flutter.dev/get-started/test-drive)
- web app : https://docs.flutter.dev/get-started/web

```
flutter devices
flutter create myapp
flutter run -d chrome
flutter build web
---
flutter config --enable-macos-desktop
flutter run -d macos
sudo gem install cocoapods
flutter create myapp
---
flutter config --enable-android
```

- [Write your first Flutter app, part 1 Flutter](https://docs.flutter.dev/get-started/codelab)
	- hot reload : https://docs.flutter.dev/development/tools/hot-reload
	- Navigator : https://api.flutter.dev/flutter/widgets/Navigator-class.html
	- WillPopScope
		- https://zonble.medium.com/%E6%80%8E%E6%A8%A3%E4%BD%BF%E7%94%A8-flutter-%E4%B8%AD%E7%9A%84-willpopscope-widget-ee4227f4951
		- https://book.flutterchina.club/chapter7/willpopscope.html
- package : [Dart packages](https://pub.dev)
	- https://stackoverflow.com/questions/61677387/flutter-how-use-conditional-compilation-for-platform-android-ios-web

```
flutter pub add flutter_calendar_carousel
flutter pub add sqflite
```

- widget : https://docs.flutter.dev/development/ui/widgets-intro
	- [Material Components widgets  Flutter](https://docs.flutter.dev/development/ui/widgets/material)
	- calendar : https://pub.dev/packages/flutter_calendar_carousel
		- https://github.com/dooboolab/flutter_calendar_carousel
	- https://api.flutter.dev/flutter/material/ExpansionTile-class.html
- sqlite : https://docs.flutter.dev/cookbook/persistence/sqlite
	- https://medium.com/%E5%86%8D%E4%B8%8D%E5%AF%AB%E5%B0%B1%E8%A6%81%E5%BF%98%E4%BA%86/flutter-%E4%BD%BF%E7%94%A8-sqlite-%E6%9C%AC%E5%9C%B0%E8%B3%87%E6%96%99%E5%BA%AB-b6c8a2f1f3e8
	- [SQLite REPLACE: Insert or Replace The Existing Row](https://www.sqlitetutorial.net/sqlite-replace-statement)
	- single db with tables
- build apk
	- https://docs.flutter.dev/deployment/android#enabling-material-components
	- https://ithelp.ithome.com.tw/articles/10224285
	- `flutter build apk`
	- signed apk
		- key : `"C:\Program Files (x86)\OpenJDK\jdk-8.0.262.10-hotspot\bin\keytool.exe" -genkey -v -keystore .\key.jks -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 -alias key`
- update db [sqflite/migration_example.md](https://github.com/tekartik/sqflite/blob/master/sqflite/doc/migration_example.md)
- export csv page by email : https://pub.dev/packages/flutter_email_sender
