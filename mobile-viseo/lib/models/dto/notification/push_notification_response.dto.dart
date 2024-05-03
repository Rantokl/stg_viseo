import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/notification/fbm.dto.dart';

class PushNotificationResponseDto extends BaseResponseDto {
  late FbmDto data;

  PushNotificationResponseDto():super();

  PushNotificationResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = FbmDto.fromJson(jsonData);
    }
  }
}