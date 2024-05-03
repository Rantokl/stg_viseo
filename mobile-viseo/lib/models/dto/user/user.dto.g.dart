// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

UserDto _$UserDtoFromJson(Map<String, dynamic> json) => UserDto(
      id: json['user_id'] as int,
      token: json['token'] as String?,
      refresh_token: json['refresh_token'] as String?,
      room_id: json['room_id'] as int?,
    )..name = json['name'] as String?;

Map<String, dynamic> _$UserDtoToJson(UserDto instance) => <String, dynamic>{
      'user_id': instance.id,
      'name': instance.name,
      'token': instance.token,
      'refresh_token': instance.refresh_token,
      'room_id': instance.room_id,
    };
