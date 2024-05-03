import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/devis/devis.dto.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/devis/devis_commentaire.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';
import 'package:sav/presentations/views/widgets/input/custom_input.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';

class DevisCommentaireView extends BaseStatelessView<DevisCommentaireController> {

   DevisCommentaireView({
    Key? key,
    required this.devis,
    required this.fromNotif
  }) : super(key: key, controller: Get.put(DevisCommentaireController()))
   ;

   final DevisDto devis;
   final bool fromNotif ;
   final _formKey = GlobalKey<FormState>();
   

  submit(int id, BuildContext context) async {
     if (_formKey.currentState!.validate()){
      controller.postDevisCommentaire(
        id: id,
        success: (isSucces) {
        if (isSucces) {
          _showConfirmationModal(context);
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
     
  }

  void _showConfirmationModal(BuildContext context) {
    Get.dialog(
      CustomModal.simpleModal(
          icon: SvgPicture.asset(Assets.icons.check, height: 20,),
          title: Strings.devis.commentaireNotification,
          onPressed: () {
            Navigator.of(context).pop();
            Get.back();
          }
          ),
      barrierDismissible: false,
    );
  }


  @override
  Widget build(BuildContext context) {

    List text = [
     {
       "text": "Merci de fournir en détails vos commentaires pour le devis n°${devis.numero_devis} du véhicule séléctionné",
       "size": 15.0,
       "isBold": true,
     },
     {
       "text": Strings.devis.commentaireRequired,
     }
   ];

    return baseScaffoldView(
        appBarController: AppBarController(
            title: Strings.devis.commentaireTitle
        ),
        withHeader: true,
        fromNotif: fromNotif,
      body: Obx(() =>
      controller.isLoading && controller.commentaireCrtl== ""
          ? Container()
          : Expanded(
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
                          CustomInput(line: 10, label: Strings.devis.commentairePlaceholder, controller: controller.commentaireCrtl ),
                          Padding(
                            padding: const EdgeInsets.symmetric(vertical: 10),
                            child: CustomeButton.elevated(fontSize: ThemeSpacing.m, buttonTitle: Strings.common.send, onPressed: () => submit(devis.devis_id, context), color: ThemeColors.green),
                          ),
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
