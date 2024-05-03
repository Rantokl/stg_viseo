import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/user/user.dto.dart';

class UserResponseDto extends BaseResponseDto {
  late UserDto data;

  UserResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = UserDto.fromJson(jsonData);
    }
  }
}