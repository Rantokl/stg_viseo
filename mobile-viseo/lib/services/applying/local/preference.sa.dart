import 'dart:convert';

import 'package:get/get.dart';
import 'package:sav/common/utils/string.extension.dart';
import 'package:sav/models/dto/devis/devis.dto.dart';
import 'package:sav/models/dto/user/profile.dto.dart';
import 'package:sav/models/dto/user/user.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle_response.dto.dart';
import 'package:shared_preferences/shared_preferences.dart';

class PreferenceSA {

  final _keyToken = "token";
  final _keyRefreshToken = "refresh_token";
  final _keyUser = "user";
  final _keyVehicle = "vehicle";
  final _keyVehicleNotif = "vehicleNotif";
  final _keyImage = "image";
  final _keyProfile = "profile";

  SharedPreferences? _preferences;

  static final PreferenceSA _instance = PreferenceSA._internal();

  VehicleDto? vehicleRdv;

  factory PreferenceSA() => _instance;

  PreferenceSA._internal();

  static PreferenceSA get instance => PreferenceSA();

  initialize() async {
    _preferences = await SharedPreferences.getInstance();
  }

  clearAll() async {
    await _preferences!.clear();
    notifLenght.value = 0;
  }

  _setString(String key, String value) {
    _preferences?.setString(key, value);
  }

  _getString(String key) => _preferences?.getString(key) ?? "";

  _setInt(String key, int value) {
    _preferences?.setInt(key, value);
  }

  _getInt(String key) => _preferences?.getInt(key) ?? 0;

  _setBool(String key, bool value) {
    _preferences?.setBool(key, value);
  }

  _getBool(String key) => _preferences?.getBool(key) ?? false;


  set token(String value) {
    _setString(_keyToken, value);
  }

  String get token => _getString(_keyToken);

  set refreshToken(String value) {
    _setString(_keyRefreshToken, value);
  }

  String get refreshToken => _getString(_keyRefreshToken);

  set user(UserDto? value) {
    _setString(_keyUser, jsonEncode(value?.toJsonLocal()));
  }

  UserDto? get user => _getUser();

  UserDto? _getUser() {
    String json = _getString(_keyUser);
    if (json.isNullOrEmpty()) {
      return null;
    } else {
      Map user = jsonDecode(json);
      return UserDto.fromJson(user);
    }
  }

  set profile(ProfileDto? value) {
    _setString(_keyProfile, jsonEncode(value?.toJsonLocal()));
  }

  ProfileDto? get profile => _getProfile();

  ProfileDto? _getProfile() {
    String json = _getString(_keyProfile);
    if (json.isNullOrEmpty()) {
      return null;
    } else {
      Map user = jsonDecode(json);
      return ProfileDto.fromJson(user);
    }
  }

  bool get isLogged => user != null;

  set vehicle(VehicleDto? vehicle) {
    _setString(_keyVehicle, jsonEncode(vehicle?.toJsonLocal()));
  }

  VehicleDto? get vehicle => _getVehicle();

  VehicleDto? _getVehicle() {
    String json = _getString(_keyVehicle);
    if (json.isNullOrEmpty()) {
      return null;
    } else {
      Map vehicle = jsonDecode(json);
      return VehicleDto.fromJson(vehicle);
    }
  }

  set vehicleNotif(VehicleDto? vehicle) {
    _setString(_keyVehicleNotif, jsonEncode(vehicle?.toJsonLocal()));
  }

  VehicleDto? get vehicleNotif => _getVehicleNotif();

  VehicleDto? _getVehicleNotif() {
    String json = _getString(_keyVehicleNotif);
    if (json.isNullOrEmpty()) {
      return null;
    } else {
      Map vehicle = jsonDecode(json);
      return VehicleDto.fromJson(vehicle);
    }
  }

  
  // DevisDto? devisNotif = Rx<DevisDto?>(null);

  set image(String image) {
    _setString(_keyImage, image);
  }

  String get image => _getImage();

  String _getImage() {
    String json = _getString(_keyImage);
    return json;
  }

  RxInt notifLenght = 0.obs; 

}