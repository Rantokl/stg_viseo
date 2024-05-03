// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'notification.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

NotificationDto _$NotificationDtoFromJson(Map<String, dynamic> json) =>
    NotificationDto(
      notif_id: json['notif_id'] as int,
      vehicle:
          (json['vehicle'] as List<dynamic>).map(VehicleDto.fromJson).toList(),
      details:
          (json['details'] as List<dynamic>).map(DevisDto.fromJson).toList(),
      isRead: json['isRead'] as bool,
      type: json['type'] as String,
      titre: json['titre'] as String,
      alerte_message: json['alerte_message'] as String,
      date_notification: json['date_notification'] as String,
    );

Map<String, dynamic> _$NotificationDtoToJson(NotificationDto instance) =>
    <String, dynamic>{
      'notif_id': instance.notif_id,
      'vehicle': instance.vehicle,
      'details': instance.details,
      'isRead': instance.isRead,
      'type': instance.type,
      'titre': instance.titre,
      'alerte_message': instance.alerte_message,
      'date_notification': instance.date_notification,
    };
