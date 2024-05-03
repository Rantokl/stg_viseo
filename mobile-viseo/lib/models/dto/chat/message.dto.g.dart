// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'message.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

MessageDto _$MessageDtoFromJson(Map<String, dynamic> json) => MessageDto(
      sender: json['sender'] as int,
      message_text: json['message_text'] as String,
      time: json['time'] as String,
    );

Map<String, dynamic> _$MessageDtoToJson(MessageDto instance) =>
    <String, dynamic>{
      'sender': instance.sender,
      'message_text': instance.message_text,
      'time': instance.time,
    };
