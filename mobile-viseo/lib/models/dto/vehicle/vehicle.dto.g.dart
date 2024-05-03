// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'vehicle.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

VehicleDto _$VehicleDtoFromJson(Map<String, dynamic> json) => VehicleDto(
      vehicle_id: json['vehicle_id'] as int,
      number: json['number'] as String?,
      model: json['model'] as String,
      specification: json['specification'] as String?,
      image: json['image'] as String?,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$VehicleDtoToJson(VehicleDto instance) =>
    <String, dynamic>{
      'vehicle_id': instance.vehicle_id,
      'number': instance.number,
      'model': instance.model,
      'specification': instance.specification,
      'image': instance.image,
      'owner_id': instance.owner_id,
    };
