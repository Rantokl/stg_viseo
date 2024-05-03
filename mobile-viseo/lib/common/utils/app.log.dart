import 'dart:developer';

class AppLog {
  static final AppLog _instance = AppLog._internal();

  factory AppLog() {
    return _instance;
  }

  AppLog._internal();

  static AppLog get instance => AppLog();

  void print({String tag = "", dynamic data}){
    log('VISEO LOG - $tag: $data');
  }
}