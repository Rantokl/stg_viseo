import 'dart:async';
import 'dart:io';

import 'package:connectivity/connectivity.dart';
import 'package:flutter/material.dart';

class ConnectionST {

  static final ConnectionST _instance = ConnectionST._internal();

  ConnectionST._internal();

  static ConnectionST get instance => _instance;

  factory ConnectionST() {
    return _instance;
  }

  final Connectivity connectivity = Connectivity();

  ConnectivityResult connectivityResult = ConnectivityResult.none;

  bool get isMobileConnection =>
      connectivityResult == ConnectivityResult.mobile;

  bool get isWifiConnection =>
      connectivityResult == ConnectivityResult.wifi;

  bool get hasConnection =>
      connectivityResult == ConnectivityResult.mobile
          || connectivityResult == ConnectivityResult.wifi;

  StreamController connectionChangeController = StreamController.broadcast();

  String get urlToCheck {
    var url = //ApiUrls.base
    "https://www.google.com/".replaceAll("http://", "")
        .replaceAll("https://", "");

    if (url[url.length - 1] == '/') {
      url = url.substring(0, url.length - 1);
    }
    return url;
  }

  initialize() async {
    var result = await checkConnection(urlToCheck: urlToCheck);
    _onConnectionChange(result);
    connectivityObserver(
        onChanged: (result) {
          _onConnectionChange(result);
        },
        urlToCheck: urlToCheck
    );
  }

  Stream get connectionChange => connectionChangeController.stream;

  ///   A clean up method to close our StreamController
  ///   Because this is meant to exist through the entire application life cycle this isn't
  ///   really an issue
  dispose() {
    connectionChangeController.close();
  }

  _onConnectionChange(result) {
    if (this.connectivityResult != result) {
      this.connectivityResult = result;
      connectionChangeController.add(hasConnection);
    }
  }

  Future<ConnectivityResult> checkConnection({
    required urlToCheck
  }) async {
    var connectivityResult = await (connectivity.checkConnectivity());
    if ((connectivityResult == ConnectivityResult.mobile)
        || (connectivityResult == ConnectivityResult.wifi)
    ) {
      if(await _internetAccess(urlToCheck)) {
        return connectivityResult;
      }
    }
    return ConnectivityResult.none;
  }

  connectivityObserver({
    required ValueChanged<ConnectivityResult> onChanged,
    required urlToCheck
  }) {
    connectivity.onConnectivityChanged.listen((
        ConnectivityResult result) async {
      // Got a new connectivity status!
      if ((result == ConnectivityResult.mobile
          || result == ConnectivityResult.wifi)
          && await _internetAccess(urlToCheck)) {
        onChanged?.call(result);
      } else {
        onChanged?.call(ConnectivityResult.none);
      }
    });
  }

  Future<bool> _internetAccess(url) async {
    try {
      final result = await InternetAddress.lookup(url);
      if (result.isNotEmpty && result[0].rawAddress.isNotEmpty) {
        return true;
      }
    } on SocketException catch (_) {
      return false;
    }
    return false;
  }
}