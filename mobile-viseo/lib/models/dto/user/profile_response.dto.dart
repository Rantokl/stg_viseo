import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/user/profile.dto.dart';

class ProfileResponseDto extends BaseResponseDto {
  late ProfileDto data;

  ProfileResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = ProfileDto.fromJson(jsonData);
    }
  }
}