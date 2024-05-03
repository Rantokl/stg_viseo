import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/mdpOublier/email.dto.dart';
import 'package:sav/models/dto/mdpOublier/mdp_oublier_reponse.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/remote/mdpOublier/mdp_oublier_remote.sa.dart';

class MdpOublierController extends BaseController {
  late MdpOublierRemoteSA service;

  String email = '';

  EmailDto request = EmailDto(from_user: "");

  late MdpOublierResponseDto response ;

  var messageResponse = "".obs;

  @override
  onInit() {
    super.onInit();
    this.service = MdpOublierRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  postEmail({
    required CompletionClosure<bool> success,
    CompletionClosure<String>? failure
  }) async {
    loading(true);
    await service.postEmail(
        email: request,
        onSuccess: (reponse) {
          response = reponse;
          loading(false);
          success?.call(true);
        },
        onFailure: (message) {
          loading(false);
          messageResponse.value = message;
          failure?.call(message);
        }
    );
  }

  onValidEmail(String value){
    request.from_user = value;
  }

  String? mailValidator(String? value){
    if (value == null || value.isEmpty) {
      return Strings.common.fieldRequired;
    }

    if (!GetUtils.isEmail(value)) {
      return Strings.common.mailNotValid;
    }

    onValidEmail(value);

    return null;
  }
}