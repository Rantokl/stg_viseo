import 'package:sav/presentations/controllers/base.controller.dart';

class SplashController extends BaseController {
  bool isAutheticate() {
    if(userLogged != null) {
      return true;
    } else {
      return false;
    }
  }

  @override
  onInit() {
    super.onInit();
  }

}