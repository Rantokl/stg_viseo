// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'owner.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

OwnerDto _$OwnerDtoFromJson(Map<String, dynamic> json) => OwnerDto(
      vehicle_id: json['vehicle_id'] as int,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$OwnerDtoToJson(OwnerDto instance) => <String, dynamic>{
      'vehicle_id': instance.vehicle_id,
      'owner_id': instance.owner_id,
    };
