

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/vehicle/search_vehicule_response.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/user_remonte.sa.dart';
import 'package:sav/services/applying/remote/vehicle/vehicule_remote.sa.dart';

import '../../../models/constant/values/strings.dart';

class VehiculeController extends BaseController {
  late VehiculeRemoteSA service;
  PreferenceSA pref = PreferenceSA.instance;
  RxBool isLoaded = false.obs;
  late Rx<VehiculeResponseDto?> userCar = Rx<VehiculeResponseDto?>(null);
  late Rx<VehiculeResponseDto?> searchCar = Rx<VehiculeResponseDto?>(null);
  final TextEditingController searchbarcrtl = TextEditingController();

  @override
  void onInit() {
    super.onInit();
    this.service = VehiculeRemoteSA();
  }

  @override
  onReady() {
    super.onReady();
  }

  RxBool isTokenExpired = false.obs;

  getUserCar({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
}) async {
    loading(true);
    await service.getUserCar(
      id: pref.user!.id,
      onSuccess: (response) {
        userCar.value = response;
        success.call(true);
      },
      onFailure: (response) {
        if (response.statusCode == Strings.common.expiredTokenCode){
          UserRemoteSA().logout();
          isTokenExpired.value = true;
          loading(false);
          failure?.call(response);
        }else{
          loading(false);
          failure?.call(response);
        }
      },
    );
    loading(false);
  }

  getSearchCar(
    String number
  ) async {
          await service.getSearchCar(
            number: number,
            onSuccess: (response) {
              searchCar.value = response;
              print("searchCar : ${searchCar.value!.data.length}");
            },
            onFailure: (error) {
              searchCar.value = null;
              print("error: $error");
            },
          );
    }


    addPref(String img) {
      pref.image = img;
    }
}


