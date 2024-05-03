import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/rdv/mes_rdv_response.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/rdv/rdv_remote.sa.dart';
import 'package:sav/services/applying/remote/vehicle/vehicule_remote.sa.dart';

import '../../../common/utils/app.utils.dart';
import '../../../models/dto/base_response.dto.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class MesRdvController extends BaseController {
  MesRdvController() : super();
  late RdvRemoteSA service;
  late VehiculeRemoteSA serviceVehicle;
  late Rx<MesRdvResponseDto?> userRdv = Rx<MesRdvResponseDto?>(null);
  late Rx<VehiculeResponseDto?> vehicule = Rx<VehiculeResponseDto?>(null);
  PreferenceSA pref = PreferenceSA.instance;

  @override
  void onInit() {
    super.onInit();
    this.service = RdvRemoteSA();
    this.serviceVehicle = VehiculeRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  getMesRdv({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
}) async {
    loading(true);
    await service.getMesRdv(
        onSuccess: (response) {
          userRdv.value = response;
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

  addVehicleToPref(VehicleDto vehicule) async{
    pref.vehicleNotif = vehicule;
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

  List<String> getStatus(String status) {
    if (status == Strings.statut.validated) {
      return [Assets.icons.check, status];
    } else if (status == Strings.statut.waiting) {
      return [Assets.icons.dots, status];
    }
    return [Assets.icons.minus, status];
  }

}