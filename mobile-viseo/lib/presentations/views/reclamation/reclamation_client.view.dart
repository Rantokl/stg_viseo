import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/reclamation/type_reclamation.dto.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/reclamation/reclamation_client.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';
import 'package:sav/presentations/views/widgets/input/custom_input.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';

import '../../../models/constant/routes.dart';

class ReclamationClientView extends BaseStatelessView<ReclamationClientController> {

  late double _screenWidth;
  late double _screenHeight;
  final _formKey = GlobalKey<FormState>();


  ReclamationClientView({
    Key? key,
  }) : super(key: key, controller: Get.put(ReclamationClientController()));

  Future<void> submit(BuildContext context) async {
    if (_formKey.currentState!.validate()) {
        controller.postReclamationClient(
          success: (isSucces) {
            if (isSucces) {
              _showConfirmationModal(context);
            }
          },
          failure: (response){
            if (response.statusCode == Strings.common.expiredTokenCode) {
              showTokenExpiredModal();
            }
            else {
              showErrorDialog(title: Strings.common.error, message: controller.messageResponse);

            }
          });
    }
  }

  void _showConfirmationModal(BuildContext context) {
    Get.dialog(
      CustomModal.simpleModal(
          icon: SvgPicture.asset(Assets.icons.check, height: 20,),
          title: Strings.reclamation.notificationTitle,
          onPressed: ()
          {
            Navigator.of(context).pop();
            Get.back();
          }
      ),
      barrierDismissible: false,
    );
  }

  @override
  Widget build(BuildContext context) {
    _screenWidth = MediaQuery.of(context).size.width;
    _screenHeight = MediaQuery.of(context).size.height;
    return baseScaffoldView(
      appBarController: AppBarController(
          title: Strings.reclamation.reclamationTitle
      ) ,
      withHeader: true,
      body: Obx(() =>
      (controller.isLoading && controller.selectedTypeReclamation.libelle == "")
          ? Container()
          : Expanded(
        child: SingleChildScrollView(
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
                        CustomeButton.dropDown<TypeReclamationDto>(
                          label: Strings.reclamation.typeReclamation,
                          item:  controller.typeReclamation.value!.data,
                          maxHeight: 200,
                          icon: Icon(Icons.keyboard_arrow_down_outlined),
                          changeItem: (dynamic newValue) {
                            controller.selectedTypeReclamation = newValue;
                          },
                          validator: controller.dropdownTypeReclamationValidator
                        ),

                        CustomInput(line: 10, label: Strings.reclamation.reclamationPlaceholder, controller: controller.messageReclamationCtrl),
                        Padding(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          child: CustomeButton.elevated(
                              fontSize: ThemeSpacing.m,
                              buttonTitle: Strings.common.send,
                              onPressed: () => submit(context),
                              color: ThemeColors.green),
                        ),
                      ],
                    ),
                  ),
                )
              ],
            ),
          ),
        ),
      )
      ),
    );
  }
}
