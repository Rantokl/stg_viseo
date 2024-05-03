import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/devis/devis_validation_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/devis/devis_remote.sa.dart';

import '../../../models/constant/values/strings.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class DevisPdfController extends BaseController {

  late DevisRemoteSA service;
  PreferenceSA pref = PreferenceSA.instance;
  late Rx<DevisValidationResponseDto?> devisDto = Rx<DevisValidationResponseDto?>(null);
  var messageResponse = "";
  @override
  onInit() {
    super.onInit();
    this.service = DevisRemoteSA();
  }

  validation({
    required int id,
    required int validation,
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
  }) async {
    loading(true);
    await service.devisValidation(
      id: id,
      validation: validation,
      onSuccess: (response) {
        devisDto.value = response;
        loading(false);
        success.call(true);
      },
      onFailure: (response) {
        if (response.statusCode == Strings.common.expiredTokenCode){
          UserRemoteSA().logout();
          loading(false);
          failure?.call(response);
        }else{
          print(response);
          messageResponse = response.message;
          loading(false);
          failure?.call(response);
        }
      },
    );
  }
  
}