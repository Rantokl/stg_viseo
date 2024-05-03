import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/notification/read_notification.dto.dart';

class ReadNotificationResponseDto extends BaseResponseDto {
  late ReadNotificationDto data;

  ReadNotificationResponseDto():super();

  ReadNotificationResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = ReadNotificationDto.fromJson(jsonData);
    }
  }
}