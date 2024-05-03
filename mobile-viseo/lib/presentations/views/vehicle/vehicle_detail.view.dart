import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/vehicle/vehicle_detail.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';

import '../widgets/modal/modal.widget.dart';

class VehicleDetailView extends BaseStatelessView<VehicleDetailController> {
  VehicleDetailView({Key? key}): super(key: key,controller: Get.put(VehicleDetailController())){
    WidgetsBinding.instance!.addPostFrameCallback((_) {
      controller.getVehicleDetail(
          success: (success) {

          },
          failure: (response) {
            if (response.statusCode == Strings.common.expiredTokenCode){
              showTokenExpiredModal();
            }
          }
      );
    });
  }

  List itemIco = [
    {
      'index': 0,
      'icon': Icon(Icons.note_add_outlined),
      'route' : Routes.vehiclePriseRdv,
      'arguments': {"rdv": null, "fromMesRdv": false}
    },
    {
      'index': 1,
      'icon': Icon(Icons.checklist_rtl_outlined),
      'route' : Routes.suiviSav,
      'arguments': null
    },
    {
      'index': 2,
      'icon': Icon(Icons.content_paste_go_outlined),
      'route' : Routes.vehicleDemandeDevis,
      'arguments': null
    },
    {
      'index': 3,
      'icon': Icon(Icons.event_note_outlined),
      'route' : Routes.listDevis,
      'arguments': null
    },
    {
      'index': 4,
      'icon': Icon(Icons.handyman_outlined),
      'route' : Routes.contratEntretien,
      'arguments': null
    },
    {
      'index': 5,
      'icon': Icon(Icons.email_outlined),
      'route' : Routes.reclamationClient,
      'arguments': null
    },
    {
      'index': 6,
      'icon': Icon(Icons.book_outlined),
      'route' : Routes.carnetGarantie,
      'arguments': null
    },
    {
      'index': 7,
      'icon': Icon(Icons.playlist_add_check, size: 30,),
      'route' : Routes.livraisonCheck,
      'arguments': null
    },
  ];

@override
  Widget build(BuildContext context) {
    double textScale = MediaQuery.of(context).textScaleFactor;
    return baseScaffoldView(
        appBarController: AppBarController(
            title: Strings.vehicle.ficheVehicle
        ),
        withHeader: true,
        withImage: true,
        body: Obx(() =>
          controller.isLoading ?
          Container() : controller.isTokenExpired.value ? Container() :
              Expanded(
                child: Container(
                  color: ThemeColors.background,
                  child: ScrollConfiguration(
                    behavior: ScrollBehavior(),
                    child: GlowingOverscrollIndicator(
                      axisDirection: AxisDirection.down,
                      color: ThemeColors.black,
                      child: GridView.builder(
                        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisSpacing: 10,
                          mainAxisSpacing: 5,
                          crossAxisCount: 2,
                          childAspectRatio: 1.55 / textScale,
                        ),
                        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                        itemCount: controller.vehicle.value!.data.menus.length,
                        itemBuilder: (context, index) {
                          var menuItem = controller.vehicle.value!.data.menus[index];
                          return CustomeButton.card(
                            buttonTitle: menuItem.menu, 
                            icon: itemIco[index]['icon'],
                            onPressed: () {
                              pushNamed(
                                routeName: itemIco[index]['route'],
                                arguments: itemIco[index]['arguments'],
                              );
                            }
                          );
                        },
                      ),
                    ),
                  ),
                ),
              )
          ),
        );
  }
}