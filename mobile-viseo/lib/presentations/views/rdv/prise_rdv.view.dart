import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/rdv/mes_rdv.dto.dart';
import 'package:sav/models/dto/rdv/type_rdv.dto.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/rdv/mes_rdv.controller.dart';
import 'package:sav/presentations/controllers/rdv/prise_rdv.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/rdv/mes_rdv.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';
import 'package:sav/presentations/views/widgets/input/custom_input.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';

import '../../../models/constant/routes.dart';

class PriseRdvView extends BaseStatelessView<PriseRdvController> {

  late double _screenWidth;
  late double _screenHeight;
  final _formKey = GlobalKey<FormState>();

  late MesRdvDto? monRdv;
  late bool fromMesRdv;

  PriseRdvView({
    Key? key
  }) : super(key: key, controller: Get.put(PriseRdvController())){
    WidgetsBinding.instance!.addPostFrameCallback((_) async {
      await controller.getTypeRdv(
          success: (success) {
            controller.getDateActuel();
            if (fromMesRdv){
              var res = controller.typeRdv.value!.data.firstWhere((element) => element.libelle == monRdv!.type_rdv);
              controller.typeRdvItemChanged(res);
              controller.messageRdvCtrl.text = monRdv!.message;
              controller.dateRendezVous.value = DateTime.parse(monRdv!.date_rdv);
              List<String> parts = monRdv!.heure_rdv.split(':');
              int hour = int.parse(parts[0]);
              int minute = int.parse(parts[1]);
              controller.getHeurePrise(success: (isSuccess){
                controller.selectedTime = TimeOfDay(hour: hour, minute: minute);
                controller.hourText.value = monRdv!.heure_rdv.substring(0, 5);
                controller.formatedHour = '${controller.selectedTime!.hour.toString().padLeft(2, '0')}:${controller.selectedTime!.minute.toString().padLeft(2, '0')}';
                if (controller.messageHeurePriseResponse.isNotEmpty){
                  showErrorDialog(title: Strings.common.error, message: controller.messageHeurePriseResponse);
                }
              },
                  failure: (message){
                    controller.selectedTime = TimeOfDay(hour: hour, minute: minute);
                    controller.hourText.value = monRdv!.heure_rdv.substring(0, 5);
                    controller.formatedHour = '${controller.selectedTime!.hour.toString().padLeft(2, '0')}:${controller.selectedTime!.minute.toString().padLeft(2, '0')}';
                    print(message);
                  });
            }
          },
          failure: (response) {
            if (response.statusCode == Strings.common.expiredTokenCode){
              showTokenExpiredModal();
            }
          }
      );
    });
  }

  Future<void> submit(BuildContext context) async {
    /**
     * contraire : la date est sous forme d' une button, l' heure est sous forme de button s' il est vide
     * probleme : il est impossible de faire une validation d' une button
     * solution : il faut verifier si l' utilisateur a bien choisir une date et une heure
     */
    if(controller.dateRendezVous.value == null){
      Get.dialog(
        CustomModal.simpleModal(
            icon: SvgPicture.asset(Assets.icons.check, height: 20,),
            title: "",
            description: Strings.rdv.dateVide,
            onPressed: ()
            {
              Navigator.of(context).pop();
            }
        ),
        barrierDismissible: false,
      );
    }else if(controller.formatedHour.isEmpty){
      Get.dialog(
        CustomModal.simpleModal(
            icon: SvgPicture.asset(Assets.icons.check, height: 20,),
            title: "",
            description: Strings.rdv.heureVide,
            onPressed: ()
            {
              Navigator.of(context).pop();
            }
        ),
        barrierDismissible: false,
      );
    }else{
      if (_formKey.currentState!.validate()){
        if (fromMesRdv){
          controller.updateRdv(rdv_id:  monRdv!.id_rdv, success: (isSucces) {
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
        else {
          controller.postPriseRdv(success: (isSucces) {
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
    }
  }

  void _showHeureNonValideModal(BuildContext context){
    String description = "";

    if(controller.dateRendezVous.value == null) {
      description = Strings.rdv.dateVide;
    }
    else if (controller.messageHeurePriseResponse.isNotEmpty) {
      description = controller.messageHeurePriseResponse;
    }

    Get.dialog(
      CustomModal.simpleModal(
          icon: SvgPicture.asset(Assets.icons.check, height: 20,),
          title: "",
          description: description,
          onPressed: ()
          {
            Navigator.of(context).pop();
          }
      ),
      barrierDismissible: false,
    );

  }

  void _showConfirmationModal(BuildContext context) {
    var dateTime = DateTime.parse(controller.dateRendezVous.value.toString());
    var dateRdv = "${dateTime.day} ${controller.getMonthName(dateTime.month-1)} ${dateTime.year} \n à ${controller.formatedHour}";
    // var dateRdv = controller.dateRendezVous.value;
    Get.dialog(
      CustomModal.simpleModal(
          icon: SvgPicture.asset(Assets.icons.check, height: 20,),
          title: Strings.rdv.notificationTitle,
          description: Strings.rdv.notificationDescription + dateRdv,
          onPressed: ()
          {
            Navigator.of(context).pop();
            if (fromMesRdv) {
              Get.find<MesRdvController>().getMesRdv(success: (success) {
                Get.back();
              });
            }
            else {
              Get.back();
            }
          }
      ),
      barrierDismissible: false,
    );
  }

  void _showDatePicker(BuildContext context){
    showDatePicker(
      context: context,
      initialDate: controller.dateActuelle.value ?? DateTime.now(),
      firstDate: controller.dateActuelle.value ?? DateTime.now(),
      lastDate: controller.dateActuelle != null ? controller.dateActuelle.value!.add(const Duration(days: 365*50)) : DateTime.now().add(const Duration(days: 365*50)),
      builder:(context, child) {
        return Theme(data: Theme.of(context).copyWith(colorScheme: ColorScheme.light(primary: Colors.black)), child: child!,);
      },
    ).then((value){
      print(value);
      controller.changeDate(value);
      // controller.dateRendezVous.value = value.toString();
      // demande heure disponible au serveur
      controller.getHeurePrise(success: (isSuccess){
        if (controller.messageHeurePriseResponse.isNotEmpty){
          showErrorDialog(title: Strings.common.error, message: controller.messageHeurePriseResponse);
        }
      },
      failure: (message){
         print(message);
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    _screenWidth = MediaQuery.of(context).size.width;
    _screenHeight = MediaQuery.of(context).size.height;

    final args = ModalRoute.of(context)!.settings.arguments as Map;
    monRdv = args['rdv'];
    fromMesRdv = args['fromMesRdv'];

    return baseScaffoldView(
      appBarController: AppBarController(
          title: fromMesRdv ? Strings.rdv.modificationTitle : Strings.rdv.demandeTitle
      ) ,
      withHeader: true,
      fromNotif: fromMesRdv,
      body: Obx(() =>
      (controller.isLoading && controller.selectedTypeRdv.libelle == "")
          ? Container()
          : controller.isTokenExpired.value ? Container() : Expanded(
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
                        CustomeButton.dropDown<TypeRdvDto>(
                            label: Strings.rdv.typeRdv,
                            item:  controller.typeRdv.value!.data,
                            icon: Icon(Icons.keyboard_arrow_down_outlined),
                            selectedValue: controller.selectedTypeRdv,
                            changeItem: (dynamic newValue) {
                              controller.typeRdvItemChanged(newValue);

                            },
                            validator: controller.dropdownTyperdvValidator
                        ),
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Flexible(
                              child: CustomeButton.simpleButton(
                                    buttonTitle: controller.dateRdvString(),
                                    fontSize: ThemeSpacing.ml,
                                    icon: Icon(Icons.calendar_month),
                                    onPressed: () => _showDatePicker(context),
                                    isActive: controller.dateRendezVous.value !=
                                        null
                              )),
                            HorizontalSpace.s,
                            controller.dateRendezVous.value == null ?
                            Flexible(
                                child: CustomeButton.simpleButton(
                                      buttonTitle: Strings.rdv.heureRdv,
                                      fontSize: ThemeSpacing.ml,
                                      icon :  Icon(Icons.watch_later_rounded),
                                      onPressed: () => _showHeureNonValideModal(context),
                                  )
                            )
                                :
                            Flexible(
                              child: Obx((){
                                return CustomeButton.simpleButton(
                                  buttonTitle: controller.hourText.value,
                                  fontSize: ThemeSpacing.ml,
                                  icon :  Icon(Icons.watch_later_rounded),
                                  onPressed: () async {
                                    if (controller.messageHeurePriseResponse.isNotEmpty) {
                                      _showHeureNonValideModal(context);
                                    }
                                    else {
                                      controller.selectedTime = await showTimePicker(
                                        context: context,
                                        cancelText: "Annuler",
                                        confirmText: "Ok",
                                        helpText: controller.helpText.value,
                                        initialTime: controller.selectedTime ?? TimeOfDay(hour: 6, minute: 0), // Heure initiale (6h00)
                                        builder:(context, child) {
                                          return MediaQuery(
                                            data: MediaQuery.of(context).copyWith(
                                              alwaysUse24HourFormat: true,
                                            ),
                                            child: Theme(
                                              data: Theme.of(context).copyWith(
                                                useMaterial3: true,
                                                timePickerTheme: TimePickerThemeData(
                                                    dialBackgroundColor : Colors.white,
                                                    hourMinuteTextStyle: TextStyle(fontSize: 50, ),
                                                    helpTextStyle: TextStyle(fontSize: 12),
                                                ),
                                                colorScheme: ColorScheme.light(primary: Colors.black),
                                              ),
                                              child: child!,
                                            ),
                                          );
                                        },
                                      );
                                      if (controller.selectedTime != null) {
                                        if (controller.selectedTime!.hour >= 6 && controller.selectedTime!.hour <= 18){
                                          controller.selectedTime = TimeOfDay(hour: controller.selectedTime!.hour, minute: 0);
                                          controller.formatedHour = controller.selectedTime!.format(context);
                                          controller.hourText.value = controller.formatedHour;
                                        }
                                        else {
                                          controller.hourText.value = Strings.rdv.heureRdv;
                                          controller.formatedHour = "";
                                          showErrorDialog(title: Strings.common.error, message: Strings.rdv.hourIndicator);
                                        }
                                      }
                                      else {
                                        controller.hourText.value = Strings.rdv.heureRdv;
                                        controller.formatedHour = "";
                                      }
                                    }
                                  },
                                  isLoading: controller.heureLoading.value,
                                  isDisable: controller.heureLoading.value
                                );
                              })
                            )
                          ],
                        ),
                        CustomInput(line: 10, label: Strings.rdv.yourMessage, controller: controller.messageRdvCtrl),
                        Padding(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          child: CustomeButton.elevated(
                              fontSize: ThemeSpacing.m,
                              buttonTitle:  fromMesRdv ? Strings.rdv.updateRdv : Strings.rdv.confirmRdv,
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

