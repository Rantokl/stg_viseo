import 'package:get/get.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/devis/list_devis_response.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/devis/devis_remote.sa.dart';

import '../../../common/utils/app.utils.dart';
import '../../../models/dto/base_response.dto.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class ListDevisController extends BaseController {
  late DevisRemoteSA service;
  PreferenceSA pref = PreferenceSA.instance;
  late Rx<ListDevisResponseDto?> ListeDevis = Rx<ListDevisResponseDto?>(null);
  RxBool isTokenExpired = false.obs;

  @override
  onInit() {
    super.onInit();
    this.service = DevisRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  getListDevis({
    required int id,
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
  }) async {
    loading(true);
    await service.getListDevis(
      id: id,
      onSuccess: (response) {
        ListeDevis.value = response;
        loading(false);
        success?.call(true);
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


  List<String> getStatus(String status) {
    if (status == Strings.statut.validated) {
      return [Assets.icons.check, status];
    } else if (status == Strings.statut.waiting) {
      return [Assets.icons.dots, status];
    }
    return [Assets.icons.minus, status];
  }

  

}