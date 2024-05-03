import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/main.controller.dart';
import 'package:sav/presentations/controllers/panic/panic.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';

class PanicView extends BaseStatelessView<MainController>{
  PanicView({Key? key}): super(key: key,controller: Get.put(MainController()));

  List text = [
     {
       "text": Strings.menu.alertDescri,
     }
   ];

  List itemIco = [
    {
      'icon': Icon(Icons.car_crash, size: 30,),
    },
    {
      'icon': Icon(Icons.miscellaneous_services,size: 30),
    },
    {
      'icon': Icon(Icons.precision_manufacturing_outlined, size: 30),
    },
    {
      'icon': Icon(Icons.tire_repair_sharp, size: 30),
    },
    {
      'icon': Icon(Icons.quick_contacts_dialer_outlined, size: 30),
    },
  ];

  void onTap(int panic_id, String panic, BuildContext context) {
    controller.postPanic(
      panic_id: panic_id, 
      success:(isSucces) {
       if (isSucces) {
         _showConfirmationModal(context, panic);
       }
       },
       failure: (response){
         if (response.statusCode == Strings.common.expiredTokenCode){
           showTokenExpiredModal();
         }
         else {
           showErrorDialog(title: Strings.common.error, message: controller.messageResponse);
         }
      }
    );
  }

  void _showConfirmationModal(BuildContext context, String panic) {
    Get.dialog(
      CustomModal.simpleModal(
        icon: SvgPicture.asset(Assets.icons.panic, height: 20, colorFilter: const ColorFilter.mode(
                              ThemeColors.red,
                              BlendMode.srcIn,
                            ),),
        title: Strings.menu.confirmationPanic,
        description: panic,
        onPressed: () {
          Get.back();
        },
      ),
      barrierDismissible: false,
    ); 
}

  @override
  Widget build(BuildContext context) {
    double textScale = MediaQuery.of(context).textScaleFactor;
    return Column(
      children: [
        CustomCard.description(text: text),
        Obx(() =>
          controller.isLoading ?
          Container() :
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
                          mainAxisSpacing: 10,
                          crossAxisCount: 2,
                          childAspectRatio: 1.55 / textScale,
                        ),
                        padding: const EdgeInsets.symmetric(horizontal: 20),
                        itemCount: controller.menuPanic.value!.data.length,
                        itemBuilder: (context, index) {
                          var menuItem = controller.menuPanic.value!.data[index];
                          return CustomeButton.card(
                            buttonTitle: menuItem.panique_menu, 
                            icon: itemIco[index]['icon'], 
                            onPressed: () => onTap(menuItem.panique_id, menuItem.panique_menu, context)
                          );
                        },
                      ),
                    ),
                  ),
                ),
              )
          ),
      ],
    );
  }
}
