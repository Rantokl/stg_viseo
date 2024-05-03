// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'owner_chat.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

OwnerChatDto _$OwnerChatDtoFromJson(Map<String, dynamic> json) => OwnerChatDto(
      room_id: json['room_id'] as int,
      message_id: json['message_id'] as int,
    );

Map<String, dynamic> _$OwnerChatDtoToJson(OwnerChatDto instance) =>
    <String, dynamic>{
      'room_id': instance.room_id,
      'message_id': instance.message_id,
    };
