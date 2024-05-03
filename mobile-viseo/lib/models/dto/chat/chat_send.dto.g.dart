// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'chat_send.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ChatSendDto _$ChatSendDtoFromJson(Map<String, dynamic> json) => ChatSendDto(
      sender: json['sender'] as int,
      message_text: json['message_text'] as String,
    );

Map<String, dynamic> _$ChatSendDtoToJson(ChatSendDto instance) =>
    <String, dynamic>{
      'sender': instance.sender,
      'message_text': instance.message_text,
    };
