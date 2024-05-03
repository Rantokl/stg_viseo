import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/rdv/mes_rdv.dto.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/rdv/mes_rdv.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';

class MesRdvView extends BaseStatelessView<MesRdvController> {

  MesRdvView({
    Key? key,
  }) : super(key: key, controller: Get.put(MesRdvController())) {
    WidgetsBinding.instance!.addPostFrameCallback((_) {
      controller.getMesRdv(
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

  Widget buildMesRdvCard(MesRdvDto rdv, String dateRdv) {
    return CustomCard.Rdv(
      title: rdv.number_vehicle,
      description: rdv.type_rdv + " : ${rdv.message}",
      date: dateRdv + " - ${rdv.heure_rdv}",
      status: controller.getStatus(rdv.status_rdv),
    );
  }

  void onTap(MesRdvDto rdv) {
    if (rdv.status_rdv == Strings.statut.waiting) {
        controller.addVehicleToPref(rdv.vehicle.first);
        pushNamed(routeName: Routes.vehiclePriseRdv, addToBack: true, arguments: {"rdv": rdv, "fromMesRdv": true});
    }
  }

  @override
  Widget build(BuildContext context) {
    return baseScaffoldView(
      appBarController: AppBarController(
        title: Strings.rdv.mesRdvTitle,
      ),
      body: Obx(
            () => (controller.isLoading)
            ? Container()
            : controller.userRdv.value == null ?
            Expanded(
              child: Container(
                alignment: Alignment.center, // Center the text both vertically and horizontally
                child: Text(
                  Strings.rdv.noMesRdv,
                  style: TextStyle(color: ThemeColors.white),
                ),
              ),
            ) :
            Expanded(
              child: SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.only(top: 15),
                child: ListView.builder(
                shrinkWrap: true,
                physics: NeverScrollableScrollPhysics(),
                itemCount: controller.userRdv.value!.data.length,
                itemBuilder: (context, index) {
                  var rdv = controller.userRdv.value!.data[index];
                  var dateTime = DateTime.parse(rdv.date_rdv);
                  var dateRdv = "${dateTime.day} ${controller.getMonthName(dateTime.month-1)}";
                  return GestureDetector(
                      onTap: (){
                        onTap(rdv);
                      },
                      child: buildMesRdvCard(rdv, dateRdv)
                  );

                },
                        ),
              ),
                    ),
            ),
      ),
    );
  }
}
