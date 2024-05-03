import 'package:flutter/material.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/user_remonte.sa.dart';
import 'package:get/get.dart';
class BaseRemoteSA {
  String get defaultError => "Une erreur inexpliquée est survenue";

  String get token => PreferenceSA.instance.token;

  delayedAction(VoidCallback action, {int delay = 200}) {
    Future.delayed(Duration(milliseconds: delay)).then((_) {
      action?.call();
    });
  }

  _refreshToken({VoidCallback? onSuccess, VoidCallback? onFailure}) {
    UserRemoteSA().refreshToken(onSuccess: (_) {
      onSuccess?.call();
    }, onFailure: (_) {
      onFailure?.call();
    });
  }

  onSuccessCompletion<T>(
      {CompletionClosure<bool>? loading,
      CompletionClosure<T>? onSuccess,
      T? success}) {
    loading?.call(false);
    onSuccess?.call(success!);
  }

  onFailureCompletion<T>(
      {bool isUnautorized = false,
      VoidCallback? onSuccessRefreshToken,
      CompletionClosure<bool>? loading,
      CompletionClosure<T>? onFailure,
      T? failure}) {
    if (isUnautorized ?? false) {
      _refreshToken(
          onSuccess: onSuccessRefreshToken,
          onFailure: () {
            loading?.call(false);
            delayedAction(() {
              onFailure?.call(failure!);
            });
          });
    } else {
      loading?.call(false);
      delayedAction(() {
        onFailure?.call(failure!);
      });
    }
  }
}
