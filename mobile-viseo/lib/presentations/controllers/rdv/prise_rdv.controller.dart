import 'package:date_format/date_format.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/rdv/heure_prise_rdv_response.dto.dart';
import 'package:sav/models/dto/rdv/prise_rdv.dto.dart';
import 'package:sav/models/dto/rdv/type_rdv.dto.dart';
import 'package:sav/models/dto/rdv/type_rdv_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/rdv/rdv_remote.sa.dart';

import '../../../models/dto/base_response.dto.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class PriseRdvController extends BaseController {
  PriseRdvController() : super();
  PreferenceSA pref = PreferenceSA.instance;
  late Rx<DateTime?> dateActuelle = Rx<DateTime?>(null);
  late RdvRemoteSA service;
  late Rx<TypeRdvResponseDto?> typeRdv = Rx<TypeRdvResponseDto?>(null);
  late Rx<HeurePriseRdvResponseDto?> heurePriseRdv = Rx<HeurePriseRdvResponseDto?>(null);
  TextEditingController messageRdvCtrl = TextEditingController();

  TypeRdvDto selectedTypeRdv = TypeRdvDto(id: 0, libelle: "");
  Rx<bool> heureLoading = Rx<bool>(false);
  PriseRdvDto priseRdvDto = PriseRdvDto(type_rendez_vous_id: 0, date_rendez_vous: "", heure_rendez_vous: "", message: "");
  TimeOfDay? selectedTime;
  var messageResponse = "";
  var messageHeurePriseResponse = "";
  var formatedHour = "";
  Rx<String> hourText = Strings.rdv.heureRdv.obs;
  Rx<String> helpText = Strings.rdv.helpText.obs;
  RxBool isTokenExpired = false.obs;

  late Rx<DateTime?> dateRendezVous = Rx<DateTime?>(null);

  List textDescription = [
    {
      "text": Strings.rdv.demandeRequired,
    }
  ];

  @override
  void onInit() {
    super.onInit();
    this.service = RdvRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  String dateRdvString(){
    if(dateRendezVous.value == null) return Strings.rdv.dateRdv;
    return formatDate(dateRendezVous.value!, [ dd, ' ', M, ' ', yyyy]);
  }

  String? dropdownTyperdvValidator(TypeRdvDto? value){
    if (value == null) {
      return Strings.common.fieldRequired;
    }
    return null;
  }


  typeRdvItemChanged(dynamic value) async {
    selectedTypeRdv = value;
    // _getHeureDisponible();
  }

  getDateActuel() async {
    loading(true);
    await service.getDateActuel(
        onSuccess: (response){
          dateActuelle.value = DateTime.parse(response.data.date_actuelle);
        }
    );
    loading(false);
  }

  getHeurePrise({
    required CompletionClosure<bool> success,
    CompletionClosure<String>? failure
  }) async {
    messageHeurePriseResponse = "";
    helpText.value = Strings.rdv.helpText;
    hourText.value = Strings.rdv.heureRdv;
    if(dateRendezVous.value != null){
      heureLoading.value = true;
      await service.getHeurePriseRdv(
          type_rendez_vous_id: selectedTypeRdv.id,
          date_rendez_vous: formatDate(dateRendezVous.value!, [yyyy, '-', mm, '-', dd]),
          onSuccess: (response){
            heurePriseRdv.value = response;
            if (response.message.contains("quota")) {
              messageHeurePriseResponse = response.message;
            }
            else {
              helpText.value += "\n\nHeure(s) déjà prise(s) : ";
              var heures = heurePriseRdv.value!.data.map((element) => element.heure_rendez_vous).toList();
              helpText.value += heures.join(", ");
            }
            success?.call(true);

          },
          onFailure: (error){
            heurePriseRdv.value = null;
            failure?.call(error);
            print(error);
          });
      heureLoading.value = false;
    }
  }

  changeDate(DateTime? dateTime) async {
    // la format du date envoyer dans la back end devrait etre comme 'yyyy-mm-d'
    dateRendezVous.value = dateTime;
  }


  String getMonthName(int number){
    var monthNames = [
      'janvier',
      'février',
      'mars',
      'avril',
      'mai',
      'juin',
      'juillet',
      'août',
      'septembre',
      'octobre',
      'novembre',
      'décembre',
    ];
    return monthNames[number];
  }

  getTypeRdv({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
}) async {
    loading(true);
    await service.getTypeRdv(
        onSuccess: (response) {
          typeRdv.value = response;
          selectedTypeRdv = typeRdv.value!.data.first;
          success.call(true);
        },
        onFailure: (response) {
          if (response.statusCode == Strings.common.expiredTokenCode){
            UserRemoteSA().logout();
            isTokenExpired.value = true;
            loading(false);
            failure?.call(response);

          }else{
            print(response);
            loading(false);
            failure?.call(response);

          }
        }
    );
    loading(false);

  }

  postPriseRdv({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
  }
      ) async {
    loading(true);
    priseRdvDto.type_rendez_vous_id = selectedTypeRdv.id;
    priseRdvDto.date_rendez_vous = formatDate(dateRendezVous.value!, [yyyy, '-', mm, '-', dd]);
    priseRdvDto.heure_rendez_vous = formatedHour + ":00"; // Ajout de seconde pour le backend
    priseRdvDto.message = messageRdvCtrl.text.trim();
    await service.postPriseRdv(vehicleId: pref.vehicle!.vehicle_id, priseRdvDto: priseRdvDto,
        onSuccess: (res){
          messageResponse = res.message;
          loading(false);
          success?.call(true);
        },
        onFailure: (response){
          if (response.statusCode == Strings.common.expiredTokenCode){
            UserRemoteSA().logout();
            isTokenExpired.value = true;
            loading(false);
            failure?.call(response);

          }
          else {
            messageResponse = response.message;
            loading(false);
            failure?.call(response);
          }

        }
    );
  }


  updateRdv({
    required int rdv_id,
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
  }
      ) async {
    loading(true);
    priseRdvDto.type_rendez_vous_id = selectedTypeRdv.id;
    priseRdvDto.date_rendez_vous = formatDate(dateRendezVous.value!, [yyyy, '-', mm, '-', dd]);
    priseRdvDto.heure_rendez_vous = formatedHour + ":00"; // Ajout de seconde pour le backend
    priseRdvDto.message = messageRdvCtrl.text.trim();
    await service.updateRdv(vehicleId: pref.vehicleNotif!.vehicle_id, rdvId: rdv_id, priseRdvDto: priseRdvDto,
        onSuccess: (res){
          messageResponse = res.message;
          loading(false);
          success?.call(true);
        },
        onFailure: (response){
          if (response.statusCode == Strings.common.expiredTokenCode){
            UserRemoteSA().logout();
            isTokenExpired.value = true;
            loading(false);
            failure?.call(response);

          }
          else {
            messageResponse = response.message;
            loading(false);
            failure?.call(response);
          }

        }
    );
  }
}
