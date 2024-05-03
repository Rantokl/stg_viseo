// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'contrat_entretien.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ContratEntretienDto _$ContratEntretienDtoFromJson(Map<String, dynamic> json) =>
    ContratEntretienDto(
      vehicle_id: json['vehicle_id'] as int,
      pdf: json['pdf'] as String,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$ContratEntretienDtoToJson(
        ContratEntretienDto instance) =>
    <String, dynamic>{
      'vehicle_id': instance.vehicle_id,
      'pdf': instance.pdf,
      'owner_id': instance.owner_id,
    };
