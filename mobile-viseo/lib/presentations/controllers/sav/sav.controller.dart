import 'package:get/get.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/dto/sav/sav_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/sav/sav_remote.sa.dart';

import '../../../common/utils/app.utils.dart';
import '../../../models/constant/values/strings.dart';
import '../../../models/dto/base_response.dto.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class SavController extends BaseController {
  
  
  late SavRemoteSA service;
  PreferenceSA pref = PreferenceSA.instance; 
  Rx<SavResponseDto?> listSav = Rx<SavResponseDto?>(null);

  @override
  onInit() {
    super.onInit();
    this.service = SavRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  getSav({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
}) async {
    loading(true);
    await service.getSav(
      vehicle_id: pref.vehicle!.vehicle_id,
      onSuccess: (response) {
        listSav.value = response;
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
      },
    );
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


  List<String> getStatus(int status) {
    if (status == 1) {
      return [Assets.icons.dots, "En cours"];
    } else if (status == 2) {
      return [Assets.icons.minus, "Annulé"];
    }
    return [Assets.icons.check, "Terminé"];
  }
}