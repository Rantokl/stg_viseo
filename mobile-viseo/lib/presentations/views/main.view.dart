import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/presentations/controllers/main.controller.dart';
import 'package:sav/presentations/views/chat/chat_admin.view.dart';
import 'package:sav/presentations/views/profil.view.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/presentations/views/vehicle/vehicle_list.view.dart';
import 'package:sav/presentations/views/panic/panic.view.dart';
import 'package:sav/presentations/views/widgets/bottomAppBar/custom_bottom_appBar.widget.dart';

class MainView extends BaseStatelessView<MainController>{
  MainView({Key? key}): super(key: key,controller: Get.put(MainController())) {
    
  }

  @override
  Widget build(BuildContext context) { 
    return GetBuilder<MainController> (
    builder: (controller) {
      if (!controller.pref.profile!.isAdmin) {
        return Scaffold(
              backgroundColor: ThemeColors.background,
              appBar: AppBar(
                backgroundColor: ThemeColors.dark,
                centerTitle: true,
                title: ConstrainedBox(
                  constraints: BoxConstraints(maxHeight: 35, maxWidth: 200),
                  child: IndexedStack(
                    index: controller.tabIndex,
                    children: [
                      Center(child: Text('Panique'.toUpperCase(), style: const TextStyle(color: Colors.white ), textAlign: TextAlign.center)),
                      Center(child: Text('Mes véhicules'.toUpperCase(), style: const TextStyle(color: Colors.white ), textAlign: TextAlign.center)),
                      Center(child: Text('Mon Profil'.toUpperCase(), style: const TextStyle(color: Colors.white ), textAlign: TextAlign.center)), 
                      Center(child: Text('Chat'.toUpperCase(), style: const TextStyle(color: Colors.white ), textAlign: TextAlign.center))
                    ],
                  )),
                actions: [
                  Padding(
                    padding: const EdgeInsets.only(right: 10),
                    child: Obx(() => controller.pref.notifLenght.value != 0
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
                            label:  Text(controller.pref.notifLenght.value.toString()),
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
                  ),
                ],
              ),
              body:  GestureDetector(
                onTap: () {
                  FocusManager.instance.primaryFocus?.unfocus();
                },
                child: SafeArea(
                  child: IndexedStack(
                      index: controller.tabIndex,
                      children: [
                        PanicView(),
                        Padding(padding: const EdgeInsets.symmetric(horizontal: 16), child: VehiculeView()),
                        Padding(padding: const EdgeInsets.symmetric(horizontal: 16), child: ProfilView()),
                      ],
                    ),
                  ),
              ),

              bottomNavigationBar: CustomBottomAppBar(),
            );
      } else {
        return ChatAdminView();
      }
    });
  }
}