import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/models/dto/user/user.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/technical/connection.st.dart';

class BaseController extends GetxController {
  PreferenceSA prefs = PreferenceSA.instance;
  RxBool loadingState = false.obs;
  RxBool connectionState = false.obs;
  RxString onFailure = "".obs;

  bool get isLogged => prefs.isLogged;

  UserDto? get userLogged => prefs.user;

  bool get isOnline => connectionState?.value ?? false;

  bool get isConnected => connectionState?.value ?? false;

  bool get isLoading => loadingState?.value ?? false;

  VehicleDto? get vehicleSelected => prefs.vehicle;

  VehicleDto? get vehicleNotif => prefs.vehicleNotif;

  String? get vehicleImg => prefs.image;

  set vehicleSelected(VehicleDto? value) {
    prefs.vehicle = value;
  }

  set _loadingState(bool newLoadingState) {
    switch (newLoadingState) {
      case true:
        if (!isLoading) {
          this.loadingState.value = true;
        }
        break;
      case false:
        if (isLoading) {
          this.loadingState.value = false;
        }
        break;
    }
  }


  BaseController() {
    _setConnectionState(ConnectionST.instance.hasConnection);
    ConnectionST.instance.connectionChange.listen((event) {
      _setConnectionState(event);
    });
  }

  _setConnectionState(bool status) {
    connectionState.value = status;
    update();
  }

  delayedAction(VoidCallback action, {int delay = 1000}) {
    Future.delayed(Duration(milliseconds: delay)).then((_) {
      action?.call();
    });
  }

  loading(bool loadingState) {
    _loadingState = loadingState;
  }
}