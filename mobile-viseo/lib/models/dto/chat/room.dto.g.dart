// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'room.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

RoomDto _$RoomDtoFromJson(Map<String, dynamic> json) => RoomDto(
      room_id: json['room_id'] as int,
      messages:
          (json['messages'] as List<dynamic>).map(MessageDto.fromJson).toList(),
      client_id: json['client_id'] as int,
    );

Map<String, dynamic> _$RoomDtoToJson(RoomDto instance) => <String, dynamic>{
      'room_id': instance.room_id,
      'messages': instance.messages,
      'client_id': instance.client_id,
    };
