// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'carnet_garantie.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

CarnetGarantieDto _$CarnetGarantieDtoFromJson(Map<String, dynamic> json) =>
    CarnetGarantieDto(
      vehicle_id: json['vehicle_id'] as int,
      pdf: json['pdf'] as String,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$CarnetGarantieDtoToJson(CarnetGarantieDto instance) =>
    <String, dynamic>{
      'vehicle_id': instance.vehicle_id,
      'pdf': instance.pdf,
      'owner_id': instance.owner_id,
    };
