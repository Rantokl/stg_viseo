import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/presentations/controllers/splash.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/main.view.dart';

import 'auth/login.view.dart';

class SplashView extends BaseStatelessView<SplashController> {
  SplashView({Key? key}): super(key: key,controller: Get.put(SplashController())) {
    controller.delayedAction(() {
      if(controller.isAutheticate()){
        pushNamed(routeName: Routes.main, addToBack: false);
      } else {
         //pushFragment(to: LoginView(), addToBack: false);
        pushNamed(routeName:Routes.login, addToBack: false);
      }
    }, delay: 2000);
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        toolbarHeight: 0,
        elevation: 0,
        backgroundColor: Colors.transparent,
      ),
      backgroundColor: ThemeColors.primary,
      body: Container(
        constraints: BoxConstraints.expand(),
        decoration: BoxDecoration(
            image: DecorationImage(
                image: AssetImage(Assets.splash), fit: BoxFit.cover)),
        child: Center(),
      ),
    );
  }
}
