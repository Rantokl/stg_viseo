import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/main.controller.dart';
import 'package:sav/presentations/controllers/sav/sav.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';

class SavView extends BaseStatelessView<SavController>{
  SavView({Key? key}): super(key: key,controller: Get.put(SavController())){
    WidgetsBinding.instance!.addPostFrameCallback((_) {
      controller.getSav(
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
    return  baseScaffoldView(
      appBarController: AppBarController(
        title: Strings.sav.sav.toUpperCase()
      ),
      withHeader: true,
      body: Obx(() => controller.isLoading
          ? Container()
          : controller.listSav.value == null
              ? Expanded(
                  child: Container(
                    alignment: Alignment.center, // Center the text both vertically and horizontally
                    child: Text(
                      "Aucun SAV trouvé",
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
                      itemCount: controller.listSav.value!.data.length,
                      itemBuilder: (context, index) {
                        var sav = controller.listSav.value!.data[index];
                        var dateTime = DateTime.parse(sav.date_sav);
                        var dateSav = "${dateTime.day} ${controller.getMonthName(dateTime.month - 1)} ${dateTime.year}";
                        return CustomCard.sav(
                          title: sav.reference, 
                          type: sav.type_sav, 
                          date: dateSav, 
                          status: controller.getStatus(sav.status_sav_id),
                          listsav: sav.etape_sav
                          );
                      },
                    ),
                  ),
                )
              )
            );
  }
}
