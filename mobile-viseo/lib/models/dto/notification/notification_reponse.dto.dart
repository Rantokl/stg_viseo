import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/notification/notification.dto.dart';

class NotificationResponseDto extends BaseResponseDto {
  late List<NotificationDto> data;

  NotificationResponseDto():super();

  NotificationResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
        .map((item) => NotificationDto.fromJson(item))
        .toList();
    }
  }
}