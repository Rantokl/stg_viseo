import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/logout/user_logout_response.dto.dart';
import 'package:sav/models/dto/user/login.dto.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/user/profile_response.dto.dart';
import 'package:sav/models/dto/user/user_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class UserRemoteRepo {
  BaseRemoteBDL get helper => BaseRemoteBDL();

  Future<UserResponseDto> login(LoginDto request) async {
    var response = await helper.post(
        Urls.user.login,
        body: request.toJsonLocal(),
        tokenRequired: false
    );
    return UserResponseDto.fromJson(response);
  }

  Future<UserResponseDto> refreshToken(dynamic params) async {
    var response = await helper.post(
      Urls.user.refreshToken,
        body: params
    );
    return UserResponseDto.fromJson(response);
  }

  Future<BaseResponseDto> checkLifetimeToken(LoginDto request) async {
    var response = await helper.post(
        Urls.user.check_lifetime_token,
    );
    return BaseResponseDto.fromJson(response);
  }

  Future<ProfileResponseDto> getProfile(int idUser) async {
    var response = await helper.get(
        "${Urls.user.profile}/$idUser/",
    );
    return ProfileResponseDto.fromJson(response);
  }

  Future<UserLogoutResponseDto> logout(int idUser) async {
    var response = await helper.post(
        "${Urls.user.logout}/$idUser/",
        tokenRequired: false
    );
    return UserLogoutResponseDto.fromJson(response);
  }
}