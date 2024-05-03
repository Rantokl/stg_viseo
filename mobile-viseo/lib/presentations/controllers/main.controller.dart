import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/evaluation/question_response.dto.dart';
import 'package:sav/models/dto/evaluation/list_question_result.dto.dart';
import 'package:sav/models/dto/link/link_reponse.dto.dart';
import 'package:sav/models/dto/panic/panic_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/presentations/views/auth/login.view.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/evaluation/evaluation_remote.SA.dart';
import 'package:sav/services/applying/remote/link/link_remote.sa.dart';
import 'package:sav/services/applying/remote/notification/notification_remote.sa.dart';
import 'package:sav/services/applying/remote/panic/panic_remote.sa.dart';
import 'package:sav/services/applying/remote/user_remonte.sa.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../models/constant/values/strings.dart';

class MainController extends BaseController {
  
  var tabIndex = 1;

  late UserRemoteSA serviceAuth;

  late PanicRemoteSA servicePanic;
  PreferenceSA pref = PreferenceSA.instance; 
  Rx<PanicResponseDto?> menuPanic = Rx<PanicResponseDto?>(null);
  var messageResponse = "";
  

  late NotificationRemoteSA serviceNotif;
  RxInt notiflenght = 0.obs;

  late LinkRemoteSA serviceLink;
  Rx<LinkResponseDto?> link = Rx<LinkResponseDto?>(null);
  
  launchURL() async {
   final Uri url = Uri.parse(link.value!.data.link);
   if (!await launchUrl(url, mode: LaunchMode.externalApplication)) {
        throw Exception('Could not launch $url');
    }
  }
  
  @override
  onInit() {
    super.onInit();
    this.servicePanic = PanicRemoteSA();
    this.serviceNotif = NotificationRemoteSA();
    this.serviceLink = LinkRemoteSA();
    this.serviceAuth = UserRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
    getMenuPanic();
    getNotiflength();
    getLink();
  }
  
  void changeTabIndex (int index)  async {
    tabIndex = index;
    update();
  }

  getMenuPanic() async {
    await servicePanic.getMenuPanic(
      onSuccess: (response) {
        menuPanic.value = response;
      },
      onFailure: (error) {
        print(error);
      },
    );
  }

  postPanic({
    required panic_id,
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
  }) async {
    loading(true);
    await servicePanic.postPanic(
      panic_id: panic_id,
      onSuccess: (res) {
          print(res.message);
          messageResponse = res.message;
          loading(false);
          success.call(true);
        },
        onFailure: (response) {
          if (response.statusCode == Strings.common.expiredTokenCode){
            UserRemoteSA().logout();
            loading(false);
            failure?.call(response);
          }
          else {
            print(response);
            messageResponse = response.message;
            loading(false);
            failure?.call(response);
          }
        }
    );
  }

  getNotiflength() async {
    await serviceNotif.getNotif(
      onSuccess: (response) {
        pref.notifLenght.value = response.data.length;
      },
      onFailure: (error) {
        print(error);
      },
    );
  }

  getLink() async {
    await serviceLink.getLink(
      onSuccess: (response) {
        link.value = response;
        print(link.value!.data.link);
      },
      onFailure: (error) {
        print(error);
      },
    );
  }

  logout({
    required CompletionClosure<bool> success,
    CompletionClosure<String>? failure
  }) async {
    loading(true);
    await serviceAuth.logout(
      onSuccess: (res) {
          loading(false);
          success.call(true);
        },
        onFailure: (message) {
          loading(false);
          failure?.call(message);
        }
    );
  }

}