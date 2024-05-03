import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';

part 'read_notification.dto.g.dart';

@JsonSerializable()
class ReadNotificationDto extends BaseDto {
  int notification_id;
  bool read;
  int owner_id;


  
  ReadNotificationDto({required this.notification_id, required this.read, required this.owner_id});

  factory ReadNotificationDto.fromJson(dynamic json) {
    return _$ReadNotificationDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.notification_id = serializable.notification_id;
    this.read = serializable.read;
    this.owner_id = serializable.owner_id;
  }

  @override
  ReadNotificationDto copy() => ReadNotificationDto(notification_id: this.notification_id, read: this.read, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$ReadNotificationDtoToJson(this);

}