import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/evaluation/question_result.dto.dart';
import 'package:sav/presentations/controllers/main.controller.dart';
import 'package:sav/presentations/controllers/profile/profile.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';

class ProfilView extends BaseStatelessView<MainController>{
  ProfilView({Key? key}): super(key: key,controller: Get.put(MainController())) {
}


  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.only(top: 10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            CustomCard.menu(iconPath: Assets.icons.car, libelle: Strings.menu.vehicleList
            , onPressed: () => {controller.changeTabIndex(1)}),
            const Divider(
              color: ThemeColors.dark,
            ),
            CustomCard.menu(iconPath: Assets.icons.clipboardCheck, libelle: Strings.menu.mesRdv, onPressed: () => {
              pushNamed(routeName: Routes.mesRdv)
            }),
            const Divider(
              color: ThemeColors.dark,
            ),
            CustomCard.menu(iconPath: Assets.icons.clipboardList, libelle: Strings.menu.mesContacts, onPressed: () => {
              pushNamed(routeName: Routes.contact)
            }),
            const Divider(
              color: ThemeColors.dark,
            ),
            CustomCard.menu(iconPath: Assets.icons.facebook, libelle: Strings.menu.facebook, onPressed: () => {
              controller.launchURL()
            }),
            const Divider(
              color: ThemeColors.dark,
            ),
            CustomCard.menu(
              iconPath: Assets.icons.avis, 
              libelle: Strings.menu.avis, 
              onPressed: () => {
                pushNamed(routeName: Routes.evaluation)
              }),
            const Divider(
              color: ThemeColors.dark,
            ),
            CustomCard.menu(
              iconPath: Assets.icons.logout, 
              libelle: Strings.menu.deconnexion, 
              onPressed: () async {
                await controller.logout(
                  success: (isSuccess) {
                    pushNamed(routeName: Routes.login, addToBack: false);
                  }
                );
              }),
          ],
        )
    );
  }
}
