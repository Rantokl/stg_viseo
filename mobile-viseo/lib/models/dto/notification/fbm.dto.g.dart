// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'fbm.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

FbmDto _$FbmDtoFromJson(Map<String, dynamic> json) => FbmDto(
      fbm: json['fbm'] as String,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$FbmDtoToJson(FbmDto instance) => <String, dynamic>{
      'fbm': instance.fbm,
      'owner_id': instance.owner_id,
    };
