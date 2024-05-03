// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'owner_vehicle_image.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

OwnerVehicleImgDto _$OwnerVehicleImgDtoFromJson(Map<String, dynamic> json) =>
    OwnerVehicleImgDto(
      vehicle_id: json['vehicle_id'] as int,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$OwnerVehicleImgDtoToJson(OwnerVehicleImgDto instance) =>
    <String, dynamic>{
      'vehicle_id': instance.vehicle_id,
      'owner_id': instance.owner_id,
    };
