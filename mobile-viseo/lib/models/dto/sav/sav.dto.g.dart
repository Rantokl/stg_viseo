// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'sav.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

SavDto _$SavDtoFromJson(Map<String, dynamic> json) => SavDto(
      id: json['id'] as int,
      reference: json['reference'] as String,
      type_sav: json['type_sav'] as String,
      status_sav_id: json['status_sav_id'] as int,
      libelle_status_sav: json['libelle_status_sav'] as String,
      date_sav: json['date_sav'] as String,
      vehicle_id: json['vehicle_id'] as int,
      owner_id: json['owner_id'] as int,
      etape_sav: (json['etape_sav'] as List<dynamic>)
          .map(EtapesavDto.fromJson)
          .toList(),
    );

Map<String, dynamic> _$SavDtoToJson(SavDto instance) => <String, dynamic>{
      'id': instance.id,
      'reference': instance.reference,
      'type_sav': instance.type_sav,
      'status_sav_id': instance.status_sav_id,
      'libelle_status_sav': instance.libelle_status_sav,
      'date_sav': instance.date_sav,
      'vehicle_id': instance.vehicle_id,
      'owner_id': instance.owner_id,
      'etape_sav': instance.etape_sav,
    };
