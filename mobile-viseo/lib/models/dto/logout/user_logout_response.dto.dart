import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/logout/user_logout.dto.dart';
import 'package:sav/models/dto/user/user.dto.dart';

class UserLogoutResponseDto extends BaseResponseDto {
  late UserLogoutDto data;

  UserLogoutResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = UserLogoutDto.fromJson(jsonData);
    }
  }
}