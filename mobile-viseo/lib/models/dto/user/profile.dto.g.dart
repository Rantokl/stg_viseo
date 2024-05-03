// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'profile.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ProfileDto _$ProfileDtoFromJson(Map<String, dynamic> json) => ProfileDto(
      mobile: json['mobile'] as String?,
      email: json['email'] as String?,
      username: json['username'] as String,
      isAdmin: json['isAdmin'] as bool,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$ProfileDtoToJson(ProfileDto instance) =>
    <String, dynamic>{
      'mobile': instance.mobile,
      'email': instance.email,
      'username': instance.username,
      'isAdmin': instance.isAdmin,
      'owner_id': instance.owner_id,
    };
