// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'send_panic.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

SendPanicDto _$SendPanicDtoFromJson(Map<String, dynamic> json) => SendPanicDto(
      to: json['to'] as String,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$SendPanicDtoToJson(SendPanicDto instance) =>
    <String, dynamic>{
      'to': instance.to,
      'owner_id': instance.owner_id,
    };
