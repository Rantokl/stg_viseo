import 'package:sav/presentations/controllers/base.controller.dart';

class AppBarController extends BaseController {
  String? title;
  int? notif;
  bool? withAction;
  void Function()? action;
  void Function()? logout;

  AppBarController({
    this.title,
    this.notif,
    this.withAction = true,
    this.action,
    this.logout
  });
}