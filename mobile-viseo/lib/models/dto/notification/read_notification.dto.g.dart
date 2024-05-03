// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'read_notification.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ReadNotificationDto _$ReadNotificationDtoFromJson(Map<String, dynamic> json) =>
    ReadNotificationDto(
      notification_id: json['notification_id'] as int,
      read: json['read'] as bool,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$ReadNotificationDtoToJson(
        ReadNotificationDto instance) =>
    <String, dynamic>{
      'notification_id': instance.notification_id,
      'read': instance.read,
      'owner_id': instance.owner_id,
    };
