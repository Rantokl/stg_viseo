import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/services/applying/local/preference.sa.dart';

class AppBarView extends BaseStatelessView<AppBarController> implements PreferredSizeWidget{
  AppBarView({
    Key? key,
    required AppBarController controller
  }) : super(key: key, controller: controller) {}

  @override
  Size get preferredSize => Size(double.infinity, AppBar().preferredSize.height);

  PreferenceSA pref = PreferenceSA.instance;

  @override
  Widget build(BuildContext context) {
    var _screenWidth = MediaQuery.of(context).size.width;
    return AppBar(
      backgroundColor: ThemeColors.dark,
      centerTitle: true,
      title: ConstrainedBox(
        constraints: BoxConstraints(maxWidth: 200),
        child:Center(
          child: Text(controller.title!.toUpperCase(),
              style: const TextStyle(color: Colors.white),
              textAlign: TextAlign.center)
        )
      ),
      actions: [
        if (controller.withAction == true && !pref.profile!.isAdmin) 
          Obx(() => pref.notifLenght.value != 0
          ? Stack(
              children: [
                IconButton(
                  icon: const Icon(
                    Icons.notifications_none_outlined,
                    color: Colors.white,
                  ),
                  onPressed: () {
                    pushNamed(routeName: Routes.notification);
                  },
                ),
                Positioned(
                  top: 8, // Ajustez cette valeur pour le positionnement vertical
                  right: 6, // Ajustez cette valeur pour le positionnement horizontal
                  child: Badge(
                    alignment: Alignment.topRight,
                    label:  Text(pref.notifLenght.value.toString()),
                  ) 
                ),
              ],
          ) 
          : IconButton(
              icon: const Icon(
                Icons.notifications_none_outlined,
                color: Colors.white,
              ),
              onPressed: () {
                pushNamed(routeName: Routes.notification);
              },
            ),
          )
        else if (controller.withAction == true)
          IconButton(
              icon: const Icon(
                Icons.logout_outlined,
                color: Colors.white,
              ),
              onPressed: controller.logout,
            ),
        
      ],
    );
  }

}