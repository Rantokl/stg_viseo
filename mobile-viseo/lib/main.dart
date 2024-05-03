import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/technical/connection.st.dart';
import 'package:sav/services/technical/notification.st.dart';
import 'package:syncfusion_localizations/syncfusion_localizations.dart';

import 'common/utils/datetime.extension.dart';
import 'models/constant/values/strings.dart';

void main() async{
  //initialize all configs
  await _initialize();

  
    
  
  //portrait orientation only
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown]
  ).then((_){
    runApp(SavApp());
    /*PermissionST.checkPermissions(
        permissions: Permission.manageExternalStorage,
        onGranted: () {

        })*/
  });
}

_initialize() async {
  //initialize the binding on async main.
  WidgetsFlutterBinding.ensureInitialized();

  //initialize preference
  await PreferenceSA().initialize();

  //initialize connectivity observer
  await ConnectionST().initialize();

  //observe connectivity status change
  ConnectionST.instance.connectionChange.listen((status) {

  });

  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  await NotificationST().initialize();
}

class SavApp extends StatelessWidget {

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {

    return GetMaterialApp(    
      title: Strings.common.appName,
      supportedLocales: [defaultLocale],
      initialRoute: Routes.splash,
      getPages: Routes.pages,
      navigatorKey: Get.key,
      localizationsDelegates: [
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        SfGlobalLocalizations.delegate,
      ],
      theme: AppTheme.buildTheme(),
    );
  }
}

