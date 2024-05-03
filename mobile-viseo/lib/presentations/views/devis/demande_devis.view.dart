import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/devis/type_devis.dto.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/devis/demande_devis.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';
import 'package:sav/presentations/views/widgets/input/custom_input.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';

class DemandeDevisView extends BaseStatelessView<DemandeDevisController> {

  late double _screenWidth;
  late double _screenHeight;
  final _formKey = GlobalKey<FormState>();

   DemandeDevisView({
    Key? key,
  }) : super(key: key, controller: Get.put(DemandeDevisController())) {
     WidgetsBinding.instance!.addPostFrameCallback((_) {
       controller.getTypeDevis(
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

   List text = [
     {
       "text": Strings.devis.demandeIndication,
       "size": 15.0,
       "isBold": true,
     },
     {
       "text": Strings.devis.demandeRequired,
     }
   ];

  submit(BuildContext context) async {
     if (_formKey.currentState!.validate()){
      controller.postDemandeDevis(
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
        }
      );
     } 
  }

  void _showConfirmationModal(BuildContext context) {
    Get.dialog(
      CustomModal.simpleModal(
          icon: SvgPicture.asset(Assets.icons.check, height: 20,),
          title: Strings.devis.notificationTitle,
          description: Strings.devis.notificationDescription,
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
            title: Strings.devis.demandeTitle
        ),
        withHeader: true,
      body: Obx(() =>
      controller.isLoading && controller.selectedValue.libelle == ""
          ? Container()
          : controller.isTokenExpired.value ? Container() : Expanded(
            child: SingleChildScrollView(
        child: GestureDetector(
            onTap: () {
              FocusManager.instance.primaryFocus?.unfocus();
            },
            child: Column(
              children: [
                CustomCard.description(text: text),
                Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: Form(
                      key: _formKey,
                      child: Column(
                        children: [
                          CustomeButton.dropDown<TypeDevisDto>(
                            label: Strings.devis.typeDevis,
                            item: controller.typeDevis.value!.data,
                            icon: Icon(Icons.keyboard_arrow_down_outlined),
                            changeItem: (dynamic newValue) {
                              controller.selectedValue = newValue;
                            },
                            validator: controller.dropdownValidator
                          ),
                          CustomInput(line: 10, label: Strings.devis.demandePlaceholder, controller: controller.detailcrtl ),
                          Padding(
                            padding: const EdgeInsets.symmetric(vertical: 10),
                            child: CustomeButton.elevated(
                                fontSize: ThemeSpacing.m,
                                buttonTitle: Strings.devis.sendDemande,
                                onPressed: () => submit(context), color: ThemeColors.green),
                          ),
                          CustomeButton.elevated(
                              fontSize: ThemeSpacing.m,
                              buttonTitle: Strings.devis.devisList,
                              onPressed: () => pushNamed(routeName: Routes.listDevis, addToBack: false), 
                              color: ThemeColors.gray
                          )
                        ],
                      ),
                    )
                )
              ] ,
            ),
        ),
      ),
          )
      ),
    );
  }
}
