import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:sav/models/dto/garantie/carnet_garantie_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/garantie/garantie_remote.sa.dart';

import '../../../common/utils/app.utils.dart';
import '../../../models/constant/values/strings.dart';
import '../../../models/dto/base_response.dto.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class CarnetGarantieController extends BaseController {
  CarnetGarantieController() : super();
  PreferenceSA pref = PreferenceSA.instance;
  late GarantieRemoteSA service;
  late Rx<CarnetGarantieResponseDto?> carnetGarantie = Rx<CarnetGarantieResponseDto?>(null);

  var messageResponse = "";

  @override
  void onInit() {
    super.onInit();
    this.service = GarantieRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  getCarnetGarantie({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
}) async {
    loading(true);
    await service.getCarnetGarantie(
      vehicleId: pref.vehicle!.vehicle_id,
        onSuccess: (response) {
          carnetGarantie.value = response;
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