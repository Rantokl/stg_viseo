// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'reclamation_client.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ReclamationClientDto _$ReclamationClientDtoFromJson(
        Map<String, dynamic> json) =>
    ReclamationClientDto(
      type_reclamation_id: json['type_reclamation_id'] as int,
      message: json['message'] as String,
    );

Map<String, dynamic> _$ReclamationClientDtoToJson(
        ReclamationClientDto instance) =>
    <String, dynamic>{
      'type_reclamation_id': instance.type_reclamation_id,
      'message': instance.message,
    };
