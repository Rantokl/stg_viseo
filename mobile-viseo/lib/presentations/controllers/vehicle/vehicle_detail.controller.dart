import 'package:get/get.dart';
import 'package:sav/models/dto/vehicle/vehicle_detail_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/vehicle/vehicle_detail_remote.sa.dart';

import '../../../common/utils/app.utils.dart';
import '../../../models/constant/values/strings.dart';
import '../../../models/dto/base_response.dto.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class VehicleDetailController extends BaseController {
  VehicleDetailController() : super();
  Rx<VehicleDetailResponseDto?> vehicle = Rx<VehicleDetailResponseDto?>(null);
  late VehicleDetailRemoteSA service;
  PreferenceSA pref = PreferenceSA.instance;
  RxBool isTokenExpired = false.obs;

  @override
  void onInit() {
    super.onInit();
    this.service = VehicleDetailRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  getVehicleDetail(
  {
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
}
      ) async {
    loading(true);
    await service.getVehicleDetail(
        id: pref.vehicle!.vehicle_id,
        onSuccess: (response) {
          vehicle.value = response;
        },
        onFailure: (response) {
          if (response.statusCode == Strings.common.expiredTokenCode){
          UserRemoteSA().logout();
          isTokenExpired.value = true;
          loading(false);
          failure?.call(response);
          }else {
            print(response);
            loading(false);
            failure?.call(response);
          }
        }
    );
    loading(false);
  }
}
