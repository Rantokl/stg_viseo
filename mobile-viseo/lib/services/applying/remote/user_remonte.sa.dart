import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/logout/user_logout_response.dto.dart';
import 'package:sav/models/dto/user/login.dto.dart';
import 'package:sav/models/dto/user/profile_response.dto.dart';
import 'package:sav/models/dto/user/user.dto.dart';
import 'package:sav/models/dto/user/user_response.dto.dart';
import 'package:sav/repository/remote/user_remote.repo.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

class UserRemoteSA extends BaseRemoteSA {
  final repository = UserRemoteRepo();
  PreferenceSA pref = PreferenceSA.instance;

  login({
    required LoginDto request,
    required CompletionClosure<UserDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await repository.login(request);
    switch (response.succes) {
      case true:
        pref.token = response.data.token ?? "";
        pref.user = response.data;
        var profileResponse = await repository.getProfile(response.data.id);
        pref.profile = profileResponse.data;
        print(pref.profile!.toJsonLocal());
        onSuccess?.call(response.data);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

  logout({
    CompletionClosure<UserLogoutResponseDto>? onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await repository.logout(pref.user!.id);
    switch (response.succes) {
      case true:
        pref.clearAll();
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

  refreshToken({
    CompletionClosure<bool>? onSuccess,
    CompletionClosure<bool>? onFailure
  }) async {

    var params = {
      "refresh_token": pref.user!.refresh_token,
    };
    var response = await repository.refreshToken(params);

    switch (response.succes) {
      case true:
        pref.token = response.data.token!;
        pref.refreshToken = response.data.refresh_token!;
        onSuccess?.call(true);
        break;
      default:
        onFailure?.call(false);
        break;
    }
  }

  getProfile ({
    required int userId,
    required CompletionClosure<ProfileResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await repository.getProfile(userId);
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }
}