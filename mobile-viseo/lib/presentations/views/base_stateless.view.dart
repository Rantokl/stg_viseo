import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:get/get_common/get_reset.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/common/utils/app.log.dart';
import 'package:sav/common/utils/string.extension.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/presentations/views/app_bar/app_bar.view.dart';
import 'package:sav/presentations/views/widgets/card/card.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';
import 'package:sav/services/applying/local/preference.sa.dart';

import '../../models/constant/routes.dart';

abstract class BaseStatelessView<CustomController extends BaseController>
    extends StatelessWidget {
  AppLog loger = AppLog.instance;
  late final CustomController controller;
  late final bool resetOnBack;

  BaseStatelessView(
      {Key? key, required this.controller, this.resetOnBack = false})
      : super(key: key) {
    controller?.loadingState?.subject?.stream?.listen((event) async {
      loger.print(tag: "LOADING STATE... : $event");
      switch (event) {
        case true:
          await _showLoader(null);
          break;
        case false:
          _hideLoader();
          break;
      }
    });

    controller?.onFailure?.subject?.stream?.listen((event) {
      if (!event.isNullOrEmpty()) {
        showErrorDialog(message: event);
      }
    });
  }

  Widget baseScaffoldView({
    required Widget body,
    Widget? bottomSheet,
    bool withImage = false,
    AppBarController? appBarController,
    bool resizeToAvoidBottomInset = true,
    bool withHeader = false,
    bool? fromNotif = false,
  }){
    return Scaffold(
        resizeToAvoidBottomInset: resizeToAvoidBottomInset,
        appBar: (appBarController == null)? null: AppBarView(controller: appBarController),
        body: GestureDetector(
            behavior: HitTestBehavior.opaque,
            onTap: hideKeyBoard,
            child: SafeArea(
                child: Column(
                  children: [
                    withImage 
                    ? Container(
                        width: double.infinity,
                        height: 175,
                        child: AspectRatio(
                          aspectRatio: 16/9,
                          child:
                          controller.vehicleSelected!.image != null ?
                          Image.network(
                            controller.vehicleSelected!.image!,
                            fit: BoxFit.fitWidth,
                            errorBuilder: (context, error, stackTrace) {
                              // Image non chargée
                              return Image.asset(Assets.logo,
                                fit: BoxFit.fitWidth,);
                            },
                          ) : Image.asset(Assets.logo,
                            fit: BoxFit.fitWidth,),
                        ),
                      )
                    : Center(),
                    (withHeader) ? Cardwidgets.vehicleHeader(
                        number: fromNotif == false ? controller.vehicleSelected!.number ?? '' : controller.vehicleNotif!.number ?? '',
                        model: fromNotif == false ? controller.vehicleSelected!.model : controller.vehicleNotif!.model,
                        specification: fromNotif == false ? controller.vehicleSelected!.specification ?? '' : controller.vehicleNotif!.specification?? ''
                    ): Center(),
                    body
                  ],
                )
            )
        ),
      bottomSheet: bottomSheet
    );
  }

  /// show loader : controller.loadingState = true
  _showLoader(String? message) async {
    hideKeyBoard();
    //if (!controller.isLoading) {
      loger.print(tag: "SHOWING LOADER");
      Get.dialog(
          buildLoading(message),
          barrierDismissible: false
      );
    //}
  }

  showTokenExpiredModal() {
    Get.dialog(
        WillPopScope(
            child: CustomModal.simpleModal(
                icon: SvgPicture.asset(Assets.icons.warning, height: 20, colorFilter: const ColorFilter.mode(
                  ThemeColors.red,
                  BlendMode.srcIn,
                ),),
                title: Strings.common.tokenExpired,
                description: Strings.common.tokenExpiredDescription,
                onPressed: () {
                  Get.back();
                  pushNamed(
                      routeName: Routes.login,
                      addToBack: false
                  );
                }
            ),
            onWillPop: () async {
              SystemNavigator.pop();
              return false;
            }),
        barrierDismissible: false
    );
  }


  /// hide loader dialog : controller.loadingState = false
  _hideLoader() {
    //if (controller.isLoading) {
      loger.print(tag: "HIDING LOADER");
      back(
          forLoader: true,
          completion: () {
            controller.loadingState.value = false;
          });
    //}
  }

  /// Pop to previous view if exist
  /// if [closeOverlays] = true, Get.back() will close the
  /// currently open snackbar/dialog/bottomsheet AND the current page
  back(
      {VoidCallback? completion,
      bool closeOverlays = false,
      bool forLoader = false,
      Widget? to}) {
    if (!navigator!.canPop() && to != null) {
      pushFragment(to: to, addToBack: false);
    } else {
      if (!navigator!.canPop()) {
        SystemNavigator.pop();
      } else {
        Get.back(closeOverlays: closeOverlays);
        if (resetOnBack && !closeOverlays && !forLoader) {
          Get.reset();
        }
        completion?.call();
      }
    }
  }

  pushFragment(
      {required Widget to,
      Transition? transition,
      dynamic arguments,
      bool addToBack = true,
      VoidCallback? completion}) {
    // "Get.to(() => Page())" instead of "Get.to(Page())"
    if (addToBack) {
      Get.to(() => to, arguments: arguments, transition: transition)?.then((_) {
        completion?.call();
      });
    } else {
      Get.reset();
      Get.off(() => to, arguments: arguments, transition: transition)
          ?.then((_) {
        completion?.call();
      });
    }
  }

  pushNamed(
      {required String routeName,
      dynamic arguments,
      bool addToBack = true,
      VoidCallback? completion}) {
    if (addToBack) {
      Get.toNamed(
        routeName,
        arguments: arguments,
      )?.then((_) {
        completion?.call();
      });
    } else {
      Get.offNamed(routeName, arguments: arguments)?.then((_) {
        completion?.call();
      });
    }
  }

  showToast({
    String? title,
    required String message,
  }) {
    Get.snackbar(
      title ?? "",
      message,
      colorText: ThemeColors.gray,
      backgroundColor: ThemeColors.dark,
      icon: const Icon(Icons.error_outline, color: ThemeColors.iconDialog),
      duration: const Duration(seconds: 5),
      isDismissible: true,
      snackPosition: SnackPosition.BOTTOM,
      borderRadius: ThemeSpacing.s,
      margin: EdgeInsets.all(ThemeSpacing.s),
    );
  }

  showErrorDialog({String? title, required String message}) {

    if (controller.isLoading) {
      _hideLoader();
    }

    Get.snackbar(
      title ?? "",
      message,
      colorText: ThemeColors.white,
      backgroundColor: ThemeColors.red,
      icon: const Icon(Icons.error_outline, color: ThemeColors.white),
      duration: const Duration(seconds: 5),
      isDismissible: true,
      snackPosition: SnackPosition.BOTTOM,
      borderRadius: ThemeSpacing.s,
      margin: EdgeInsets.all(ThemeSpacing.s),
    );
  }

  Widget buildLoading(String? message) {
    return AlertDialog(
      backgroundColor: ThemeColors.dark,
      content: Row(
        children: [
          CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(ThemeColors.iconDialog)),
          HorizontalSpace.l,
          Expanded(
              child: Text(
                message ?? Strings.common.pleaseWait,
                style: TextStyle(
                    color: ThemeColors.gray
                ),
              )
          ),
        ],
      ),
    );
  }

  /// Hide current keyboard
  hideKeyBoard() {
    FocusManager.instance.primaryFocus?.unfocus();
  }
}
