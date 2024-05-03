import 'package:get/get_rx/src/rx_types/rx_types.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/devis/devis.dto.dart';
import 'package:sav/models/dto/notification/notification_reponse.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/repository/remote/notification/notification_remote.repo.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/notification/notification_remote.sa.dart';

import '../../../models/constant/values/strings.dart';
import '../../../models/dto/base_response.dto.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class NotificationController extends BaseController {

  late NotificationRemoteSA serviceNotif;
  PreferenceSA pref = PreferenceSA.instance; 
  Rx<NotificationResponseDto?> listNotif = Rx<NotificationResponseDto?>(null);

  @override
  onInit() {
    super.onInit();
    this.serviceNotif = NotificationRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  getNotif(
  {
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
}
      ) async {
    loading(true);
    await serviceNotif.getNotif(
      onSuccess: (response) {
        listNotif.value = response;
        print(listNotif.value!.data.length);
        loading(false);
        success?.call(true);
      },
      onFailure: (response) {
        if (response.statusCode == Strings.common.expiredTokenCode){
          UserRemoteSA().logout();
          loading(false);
          failure?.call(response);
        }else{
          print(response);
          loading(false);
          failure?.call(response);
        }
      },
    );
  }

  addPref(VehicleDto vehicle) {
      pref.vehicleNotif = vehicle;
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


  readNotif({
    required notifId,
    required CompletionClosure<bool> success,
    CompletionClosure<String>? failure
  }) async {
    loading(true);
    await serviceNotif.readNotif(
      notifId: notifId,
      onSuccess: (response) {
        if (pref.notifLenght > 0){
          pref.notifLenght -= 1;
        }
        else
        {
          pref.notifLenght = 0.obs;
        }
        loading(false);
        success.call(true);
      },
      onFailure: (error) {
        print(error);
        loading(false);
        failure?.call(error);
      },
    );
  }
}