
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/livraison/check_list_item/checkListItem.dto.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/livraison/livraison_message.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';
import 'package:sav/presentations/views/widgets/input/custom_input.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';

import '../../../models/constant/routes.dart';

class LivraisonMessageView extends BaseStatelessView<LivraisonMessageController>{
  final List<CheckListItemDto> listCheckListItemDto;
  late double _screenWidth;
  late double _screenHeight;
  final _formKey = GlobalKey<FormState>();

  
  LivraisonMessageView(this.listCheckListItemDto, {
    Key? key
  }) : super(key: key, controller: Get.put(LivraisonMessageController()));

  @override
  Widget build(BuildContext context) {
    _screenWidth = MediaQuery.of(context).size.width;
    _screenHeight = MediaQuery.of(context).size.height;
    return baseScaffoldView(
      appBarController: AppBarController(
        title: controller.vehicleSelected?.number
      ),
      withHeader: true,
      body: Obx(() => 
        controller.isLoading 
        ? Container()
        : Expanded(
            child: GestureDetector(
              onTap: (){
                FocusManager.instance.primaryFocus?.unfocus();
              },
              child: Column(
                children: [
                  CustomCard.description(text: controller.textDescription),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        children: [
                          CustomInput(line: 10, label: Strings.reclamation.reclamationPlaceholder, controller: controller.messageReclamationCtrl),
                             Padding(
                              padding: const EdgeInsets.symmetric(vertical: 10),
                              child: CustomeButton.elevated(
                              horizontal: _screenWidth,
                              fontSize: ThemeSpacing.m,
                              buttonTitle: Strings.common.send,
                              onPressed: (){
                                _showRequestConfirmationValidateModal(context);
                              },
                              color: ThemeColors.green),
                          ),
                        ]
                      ),
                    ),
                  )
                ]
              ),
            )
          )
      )
    );
  }

  submitCheckList(BuildContext context) async {
    if (_formKey.currentState!.validate()) {
      controller.postCheckListItemsWithMessage(
        listCheckListItemDto: listCheckListItemDto, 
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
  }

  void _showConfirmationModal(BuildContext context, String message){
    Get.dialog(
      CustomModal.simpleModal(
        icon: SvgPicture.asset(Assets.icons.check, height: 20,),
        title: message, 
        onPressed: (){
          Navigator.of(context).pop();
          Get.back();
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
        fontSize: 14.0,
        child: Center(
          child: Text(
            Strings.livraison.messageConfirmationWithReserve,
            textAlign : TextAlign.center,
            style: TextStyle(
              color: ThemeColors.white,
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