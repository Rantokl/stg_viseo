import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/notification/push_notification.dto.dart';
import 'package:sav/models/dto/user/login.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/remote/notification/notification_remote.sa.dart';
import 'package:sav/services/applying/remote/user_remonte.sa.dart';

class LoginController extends BaseController {
  late UserRemoteSA service;
  late NotificationRemoteSA fbmService;
  String email = '';
  String password = '';
  var isPasswordHidden = false.obs;
  var isUserAdmin = false;

  LoginDto request = LoginDto(username: '',password: '');
  PushNotificationDto fbmToken = PushNotificationDto(token: "");
  FirebaseMessaging _fcm = FirebaseMessaging.instance;

  @override
  onInit() {
    super.onInit();
    this.service = UserRemoteSA();
    this.fbmService = NotificationRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
    isPasswordHidden.value = false;
  }

  authenticate({
    required CompletionClosure<bool> success,
    CompletionClosure<String>? failure
  }) async {
    loading(true);
    await service.login(
        request: request,
        onSuccess: (user) {
          postfbm(
            success: (success) {
              print("fbm Token sent");
            },
            failure: (message) {
              print("fbm ====== $message");
            }
          );
          success?.call(true);
        },
        onFailure: (message) {
          loading(false);
          failure?.call(message);
        }
    );

  }

  onValidUserName(String value){
    request.username = value;
  }

  onValidPassword(String value){
    request.password = value;
  }

  onPasswordVisibilityChange(bool visibility){
      isPasswordHidden.value = (visibility == null) ? false : visibility;
  }

  String? usernameValidator(String? value){
    if (value == null || value.isEmpty) {
      return Strings.common.fieldRequired;
    }

    onValidUserName(value);

    return null;
  }

  postfbm({
    required CompletionClosure<bool> success,
    CompletionClosure<String>? failure
  }) async {
    fbmToken.token = await _fcm.getToken();
    print("token: ${fbmToken.token}");
    await fbmService.postfbm(
        request: fbmToken,
        onSuccess: (token) {
          success?.call(true);
        },
        onFailure: (message) {
          failure?.call(message);
        }
    );    
  }

}