// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'vehicle_detail.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

VehicleDetailDto _$VehicleDetailDtoFromJson(Map<String, dynamic> json) =>
    VehicleDetailDto(
      vehicle_id: json['vehicle_id'] as int,
      number: json['number'] as String?,
      model: json['model'] as String,
      specification: json['specification'] as String?,
      image: json['image'] as String?,
      owner_id: json['owner_id'] as int,
      menus: (json['menus'] as List<dynamic>).map(MenuDto.fromJson).toList(),
    );

Map<String, dynamic> _$VehicleDetailDtoToJson(VehicleDetailDto instance) =>
    <String, dynamic>{
      'vehicle_id': instance.vehicle_id,
      'number': instance.number,
      'model': instance.model,
      'specification': instance.specification,
      'image': instance.image,
      'owner_id': instance.owner_id,
      'menus': instance.menus,
    };
