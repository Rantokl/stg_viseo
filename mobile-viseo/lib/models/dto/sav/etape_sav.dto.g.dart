// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'etape_sav.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

EtapesavDto _$EtapesavDtoFromJson(Map<String, dynamic> json) => EtapesavDto(
      etape: json['etape'] as String,
      status_id: json['status_id'] as int,
      libelle: json['libelle'] as String,
    );

Map<String, dynamic> _$EtapesavDtoToJson(EtapesavDto instance) =>
    <String, dynamic>{
      'etape': instance.etape,
      'status_id': instance.status_id,
      'libelle': instance.libelle,
    };
