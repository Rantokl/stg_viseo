// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'owner_devis.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

OwnerDevisDto _$OwnerDevisDtoFromJson(Map<String, dynamic> json) =>
    OwnerDevisDto(
      vehicle_id: json['vehicle_id'] as int,
      owner_id: json['owner_id'] as int,
      status_id: json['status_id'] as int,
      devis_id: json['devis_id'] as int,
    );

Map<String, dynamic> _$OwnerDevisDtoToJson(OwnerDevisDto instance) =>
    <String, dynamic>{
      'vehicle_id': instance.vehicle_id,
      'owner_id': instance.owner_id,
      'status_id': instance.status_id,
      'devis_id': instance.devis_id,
    };
