import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'push_notification.dto.g.dart';

@JsonSerializable()
class PushNotificationDto extends BaseDto {
  String? token;
  
  PushNotificationDto({required this.token});

  factory PushNotificationDto.fromJson(dynamic json) {
    return _$PushNotificationDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.token = serializable.token;
  }

  @override
  PushNotificationDto copy() => PushNotificationDto(token: this.token)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$PushNotificationDtoToJson(this);

}