import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/devis/devis.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/main.controller.dart';
import 'package:sav/presentations/controllers/notification/notification.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';
import 'package:sav/services/applying/local/preference.sa.dart';

import '../../../models/constant/values/assets.dart';
import '../widgets/modal/modal.widget.dart';

class NotificationView extends BaseStatelessView<NotificationController>{
  NotificationView({Key? key}): super(key: key,controller: Get.put(NotificationController())) {
    WidgetsBinding.instance!.addPostFrameCallback((_) {
      controller.getNotif(
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

  PreferenceSA pref = PreferenceSA.instance;

  void action(String type, VehicleDto? vehicle, int notifId, DevisDto? devis) {
    controller.readNotif(
      notifId: notifId, 
      success:(success) {

        if (type == Strings.notification.notifDevis) {
          controller.addPref(vehicle!);
          pushNamed(routeName: Routes.devisPdf, addToBack: false, arguments: {"devis": devis, "fromNotif": true});
        }
        else if (type == Strings.notification.notifChat) {
          pushNamed(routeName: Routes.chat, addToBack: false, arguments: {"roomId":pref.user!.room_id, "username": "SERVICE VISEO"});
        }
        else
        {
          pushNamed(routeName: Routes.mesRdv, addToBack: false);
        }
      },
      failure: (failure) {
        showToast(message: failure);
      } 
    );
    
  }


  Widget buildNotificationCard(String type, String resume, String? model, String date) {
    var title = "";
    if (type == Strings.notification.notifDevis) {
      title = Strings.notification.notifDevis;
    } else if (type == Strings.notification.notifChat) {
      title = Strings.notification.notifChat;
    }
    else {
      title = Strings.notification.notifRdv;
    }

    return CustomCard.notif(title: title, resume: resume, date: date);
  }

  @override
  Widget build(BuildContext context) {
    return baseScaffoldView(
      appBarController: AppBarController(title: Strings.notification.notification, withAction: false),
      
      body: Obx(() => controller.isLoading
          ? Container()
          : controller.listNotif.value == null
              ? Expanded(
                  child: Container(
                    alignment: Alignment.center, 
                    child: const Text(
                      "Vous n'avez aucune notification",
                      style: TextStyle(color: ThemeColors.white),
                    ),
                  ),
                )
              : Expanded(
                  child: SingleChildScrollView(
                    child: ListView.builder(
                      shrinkWrap: true,
                      physics: NeverScrollableScrollPhysics(),
                      itemCount: controller.listNotif.value!.data.length,
                      itemBuilder: (context, index) {
                        var notif = controller.listNotif.value!.data[index];
                        var dateTime = DateTime.parse(notif.date_notification);
                        var date = "${dateTime.day} ${controller.getMonthName(dateTime.month - 1)} ${dateTime.year} - "
                            "${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}";

                        var model = notif.vehicle.isNotEmpty ? notif.vehicle.first.model : null;

                        return GestureDetector(
                          onTap: (){
                            action(notif.type, notif.vehicle.isNotEmpty ? notif.vehicle.first : null, notif.notif_id, notif.details.isNotEmpty ? notif.details.first : null);
                          },
                          child: buildNotificationCard(notif.type, notif.alerte_message, model, date)
                        );
                      },
                    ),
                  ),
                )),
    );
  }
}

