import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/devis/list_devis.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';

import '../../../models/constant/values/assets.dart';
import '../widgets/modal/modal.widget.dart';

class ListDevisView extends BaseStatelessView<ListDevisController> {
  ListDevisView({Key? key}) : super(key: key, controller: Get.put(ListDevisController())){
    WidgetsBinding.instance!.addPostFrameCallback((_) {
      controller.getListDevis(
        id: controller.vehicleSelected!.vehicle_id,
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

  @override
  Widget build(BuildContext context) {
    return baseScaffoldView(
      appBarController: AppBarController(title: Strings.devis.devisList),
      withHeader: true,
      body: Obx(() => controller.isLoading
          ? Container()
          : controller.isTokenExpired.value ? Container() : controller.ListeDevis.value == null
              ? Expanded(
                  child: Container(
                    alignment: Alignment.center, // Center the text both vertically and horizontally
                    child: Text(
                      "Aucun devis trouvé",
                      style: TextStyle(color: ThemeColors.white),
                    ),
                  ),
                )
              : Expanded(
                  // Wrap with Expanded
                  child: SingleChildScrollView(
                    child: ListView.builder(
                      shrinkWrap: true,
                      physics: NeverScrollableScrollPhysics(),
                      itemCount: controller.ListeDevis.value!.data.length,
                      itemBuilder: (context, index) {
                        var devis = controller.ListeDevis.value!.data[index];
                        var dateTime = DateTime.parse(devis.date_devis);
                        var dateDevis = "${dateTime.day} ${controller.getMonthName(dateTime.month - 1)} ${dateTime.year}";
                        return GestureDetector(
                          onTap: (){
                            devis.pdf == null ? {} : pushNamed(routeName: Routes.devisPdf, addToBack: false ,arguments: {"devis": devis, "fromNotif": false});
                          },
                          child: CustomCard.Devis(
                              title: devis.numero_devis ?? devis.type_devis,
                              resume: devis.resume ?? devis.details,
                              price: devis.prix ?? "",
                              status: controller.getStatus(devis.status_devis),
                              date: dateDevis,
                          )
                        );
                            
                      },
                    ),
                  ),
                )),
    );
  }
}
