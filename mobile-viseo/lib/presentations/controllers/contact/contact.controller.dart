import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/contact/contact_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/contact/contact_remote.sa.dart';

import '../../../common/utils/app.utils.dart';
import '../../../models/dto/base_response.dto.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class ContactController extends BaseController {
  ContactController() : super();
  late ContactRemoteSA service;
  late Rx<ContactResponseDto?> contact = Rx<ContactResponseDto?>(null);

  @override
  void onInit() {
    super.onInit();
    this.service = ContactRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
  }

  getContact(
  {
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
}
      ) async {
    loading(true);
    await service.getContact(
        onSuccess: (response) {
          contact.value = response;
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