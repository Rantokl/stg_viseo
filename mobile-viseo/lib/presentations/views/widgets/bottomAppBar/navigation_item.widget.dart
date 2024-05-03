import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/main.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/services/applying/local/preference.sa.dart';


class NavigationItem extends BaseStatelessView<MainController>{
  NavigationItem({Key? key}): super(key: key, controller: Get.put(MainController())) {
  }

  late double _screenWidth;
  late double _screenHeight;

  PreferenceSA pref = PreferenceSA.instance;

  @override
  Widget build(BuildContext context) {
    _screenWidth = MediaQuery.of(context).size.width;
    _screenHeight = MediaQuery.of(context).size.height;

    return GetBuilder<MainController> (
        builder: (controller) {
          return Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: item.map((e) {
              return GestureDetector(
                onTap: () {
                  if (e['index'] == 3) {
                    if (pref.profile!.isAdmin)
                      pushNamed(routeName: Routes.chatAdmin, addToBack: true);
                    else
                      pushNamed(routeName: Routes.chat, addToBack: true, arguments: {"roomId":pref.user!.room_id, "username": "SERVICE VISEO"});
                  }
                  else
                    controller.changeTabIndex(e['index']);
                },
                child: Container(
                  width: _screenWidth / 4.5,
                  decoration: BoxDecoration(
                    color: e['backgroundcolor'],
                    borderRadius: BorderRadius.circular(10.0),
                  ),
                  child: Container(
                    height: 70,
                    decoration: controller.tabIndex == e['index'] ? BoxDecoration(
                      color: controller.tabIndex == 0 ? ThemeColors.red : ThemeColors.dark,
                      borderRadius: BorderRadius.circular(10.0),
                    ) : null,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          height: 30,
                          child: SvgPicture.asset(
                            e['icon'],
                            colorFilter: const ColorFilter.mode(
                              Colors.white,
                              BlendMode.srcIn,
                            ),
                            height: e['height'],
                          ),
                        ),
                        Text(
                          e['label'],
                          style: TextStyle(color: Colors.white),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ),
                  ),
                ),
              );
            }).toList(),

          );
        });
  }

  List item = [
    {
      'index': 0,
      'height': 25.0,
      'backgroundcolor': ThemeColors.red,
      'icon': Assets.icons.panic,
      'label': Strings.menu.panic
    },
    {
      'index': 1,
      'height': 20.0,
      'backgroundcolor': ThemeColors.transparent,
      'icon': Assets.icons.car,
      'label': Strings.menu.vehicles
    },
    {
      'index': 2,
      'height': 20.0,
      'backgroundcolor': ThemeColors.transparent,
      'icon': Assets.icons.user,
      'label': Strings.menu.profil
    },
    {
      'index': 3,
      'height': 30.0,
      'backgroundcolor': ThemeColors.transparent,
      'icon': Assets.icons.message,
      'label': Strings.menu.chat
    },
  ];
}