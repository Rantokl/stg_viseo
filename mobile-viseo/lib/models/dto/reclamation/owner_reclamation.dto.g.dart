// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'owner_reclamation.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

OwnerReclamationDto _$OwnerReclamationDtoFromJson(Map<String, dynamic> json) =>
    OwnerReclamationDto(
      message: json['message'] as String,
      vehicle_id: json['vehicle_id'] as int,
      reclamation_id: json['reclamation_id'] as int,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$OwnerReclamationDtoToJson(
        OwnerReclamationDto instance) =>
    <String, dynamic>{
      'message': instance.message,
      'vehicle_id': instance.vehicle_id,
      'reclamation_id': instance.reclamation_id,
      'owner_id': instance.owner_id,
    };
