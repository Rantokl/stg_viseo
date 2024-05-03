import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/livraison/livraison_check.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/livraison/livraison_check_list.widget.dart';
import 'package:sav/presentations/views/livraison/livraison_message.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';

import '../../../models/constant/routes.dart';

class LivraisonCheckView extends BaseStatelessView<LivraisonCheckListController> {

  late double _screenWidth;
  late double _screenHeight;

  LivraisonCheckView({
    Key? key,
  }) : super(key: key, controller: Get.put(LivraisonCheckListController())) {
    WidgetsBinding.instance!.addPostFrameCallback((_) {
      controller.getCheckListLivraison(
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
    _screenWidth = MediaQuery.of(context).size.width;
    _screenHeight = MediaQuery.of(context).size.height;

    return baseScaffoldView(
      appBarController: AppBarController(
        title:'CHECKLIST LIVRAISON'
      ) ,
      withHeader: true,
      body:  Obx(() => 
              controller.isLoading  ? Container()
              : controller.isTokenExpired.value ? Container() : controller.checkListLivraison.value!.checkListstatus == 1 || controller.checkListLivraison.value!.checkListstatus == 2 ?
              Expanded(
                child: Container(
                  alignment: Alignment.center, // Center the text both vertically and horizontally
                  child: Text(
                    controller.checkListLivraison.value!.checkListstatus == 1 ? Strings.livraison.livraisonDejaFait : Strings.livraison.checklistReject,
                    style: const TextStyle(color: ThemeColors.white),
                  ),
                ),
              )
              : Expanded(
                child: Column(
                    children: [
                       Expanded(
                         child: ListView.builder(
                              padding: const EdgeInsets.all(10),
                              itemCount: controller.checkListLivraison.value!.data.length,
                              itemBuilder: (context, index){

                                return LivraisonCheckListWidget(
                                    checkListLivraison : controller.checkListLivraison.value!.data[index],
                                    changeCheckItem : controller.changeCheckItem, 
                                  );
                              },
                          ),
                       ),
                      _actionsButtons(context)
                    ],
                  ),
              )
            )
    );
  }

 Widget _actionsButtons(BuildContext context){
    return Padding(
      padding: const EdgeInsets.all(10),
      child: Column(
        children: [
          CustomeButton.elevated(
            horizontal: _screenWidth ,
            fontSize: ThemeSpacing.m,
            buttonTitle: Strings.common.validate,
            onPressed: (){
              _showRequestConfirmationValidateModal(context);
            } ),
          const SizedBox(height: 10,),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              CustomeButton.elevated(
                horizontal : _screenWidth / 2.25,
                fontSize: ThemeSpacing.m, 
                onPressed: (){
                  // Get.back();
                  submitResetCheckList(context);
                }, 
                buttonTitle: Strings.common.dismiss,
                color: ThemeColors.red
              ),
              
              CustomeButton.elevated(
                horizontal : _screenWidth / 2.25,
                fontSize: ThemeSpacing.m, 
                onPressed: () async {
                  pushFragment(to: LivraisonMessageView(await controller.listCheckListItemDto_extract()));
                }, 
                buttonTitle: Strings.livraison.reserve,
                color: ThemeColors.gray)
            ],
          )
        ],
      ),
    );
  }


  submitCheckList(BuildContext context) async {
    controller.postCheckListItems(
      stateId: 1,
      success: (message) {
        _showConfirmationModal(context, Strings.livraison.notivicationValidated);
      },
      failure: (response){
        if (response.statusCode == Strings.common.expiredTokenCode){
          showTokenExpiredModal();
        }
        else {
          showErrorDialog(title: Strings.common.error, message: response.message);
        }
      }
    );
  }

  submitResetCheckList(BuildContext context) async {
    controller.postCheckListItems(
      stateId : 2,
      success: (message){
        Get.back();
      },
      failure: (response){
        if (response.statusCode == Strings.common.expiredTokenCode){
          showTokenExpiredModal();
        }
        else {
          showErrorDialog(title: Strings.common.error, message: response.message);
        }
      }
    );
  }

  void _showConfirmationModal(BuildContext  context, String message){
    Get.dialog(
      CustomModal.simpleModal(
        icon: SvgPicture.asset(Assets.icons.check, height: 20,),
        title: message, 
        onPressed: () {
          Navigator.of(context).pop();
          Get.back();
        }
      ),
      barrierDismissible: false,
    );
  }

  void _showRequestConfirmationValidateModal(BuildContext context){
        Get.dialog(
      CustomModal.twoActionModal(
        context: context, 
        icon: SvgPicture.asset(Assets.icons.check, height: 20,), 
        child: Center(
          child: Text(
            Strings.livraison.messageConfirmation,
            textAlign : TextAlign.center, 
            style: const TextStyle(
              color: ThemeColors.white,
              height: 1.5
            ),
          ),
        ), 
        firstActionName: Strings.common.close, 
        onFirstActionPressed: (){
          Navigator.of(context).pop();
        }, 
        secondActionName: Strings.common.confirm, 
        onSecondActionPressed: (){
          
          Navigator.of(context).pop();
          submitCheckList(context);
        }
      )
    );
  }
}
