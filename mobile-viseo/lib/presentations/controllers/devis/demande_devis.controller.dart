import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/devis/demande_devis.dto.dart';
import 'package:sav/models/dto/devis/type_devis.dto.dart';
import 'package:sav/models/dto/devis/type_devis_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/devis/devis_remote.sa.dart';

import '../../../services/applying/remote/user_remonte.sa.dart';

class DemandeDevisController extends BaseController {
  DemandeDevisController() : super();

  late DevisRemoteSA service;
  PreferenceSA pref = PreferenceSA.instance;
  final TextEditingController detailcrtl = TextEditingController();
  Rx<TypeDevisResponseDto?> typeDevis = Rx<TypeDevisResponseDto?>(null);
  late TypeDevisDto selectedValue = TypeDevisDto(id: 0, libelle: "");
  demandeDevisDto req = demandeDevisDto(type_devis_id: 0, details: "Type de devis");
  var messageResponse = "";
  RxBool isTokenExpired = false.obs;

  @override
  void onInit() {
    super.onInit();
    this.service = DevisRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  String? dropdownValidator(TypeDevisDto? value){
    if (value == null) {
      return Strings.common.fieldRequired;
    }

    return null;
  }

  getTypeDevis({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
  }) async {
    loading(true);
    await service.getTypeDevis(
      onSuccess: (response) {
        typeDevis.value = response;
        loading(false);
      },
      onFailure: (response) {
        if (response.statusCode == Strings.common.expiredTokenCode){
          UserRemoteSA().logout();
          isTokenExpired.value = true;
          loading(false);
          failure?.call(response);

        }else{
          failure?.call(response);
          loading(false);
        }
      },
    );
  }

  postDemandeDevis({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
  }) async {
    req.details = detailcrtl.text;
    req.type_devis_id = selectedValue!.id;
    loading(true);
    await service.postDemandeDevis(
      vehicle_id: pref.vehicle!.vehicle_id,
      request: req, 
      onSuccess: (res) {
          print(res.message);
          messageResponse = res.message;
          loading(false);
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
            messageResponse = response.message;
            loading(false);
            failure?.call(response);
          }
        }
    );
  }
}