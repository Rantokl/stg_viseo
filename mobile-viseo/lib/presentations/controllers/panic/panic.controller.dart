import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/panic/panic_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/panic/panic_remote.sa.dart';

import '../../../models/constant/values/strings.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class PanicController extends BaseController {
  PanicController() : super();

  late PanicRemoteSA service;
  PreferenceSA pref = PreferenceSA.instance; 
  Rx<PanicResponseDto?> menuPanic = Rx<PanicResponseDto?>(null);
  var messageResponse = "";
  @override
  onInit() {
    super.onInit();
    this.service = PanicRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
    getMenuPanic();
  }

  getMenuPanic() async {
    loading(true);
    await service.getMenuPanic(
      onSuccess: (response) {
        menuPanic.value = response;
        loading(false);
      },
      onFailure: (error) {
        print(error);
        loading(false);
      },
    );
  }


}