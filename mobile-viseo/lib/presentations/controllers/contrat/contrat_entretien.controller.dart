import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:sav/models/dto/contrat/contrat_entretien_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/contrat/contrat_remote.sa.dart';

import '../../../common/utils/app.utils.dart';
import '../../../models/constant/values/strings.dart';
import '../../../models/dto/base_response.dto.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class ContratEntretienController extends BaseController {
  ContratEntretienController() : super();
  PreferenceSA pref = PreferenceSA.instance;
  late ContratRemoteSA service;
  late Rx<ContratEntretienResponseDto?> contratEntretien = Rx<ContratEntretienResponseDto?>(null);

  @override
  void onInit() {
    super.onInit();
    this.service = ContratRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  getContratEntretien({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
}) async {
    loading(true);
    await service.getContratEntretien(
      vehicleId: pref.vehicle!.vehicle_id,
        onSuccess: (response) {
          contratEntretien.value = response;
          loading(false);
          success.call(true);
        },
        onFailure: (response) {
          if (response.statusCode == Strings.common.expiredTokenCode){
            UserRemoteSA().logout();
            loading(false);
            failure?.call(response);
          }else{
            loading(false);
            failure?.call(response);
          }
        }
    );
  }

}