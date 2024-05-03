import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'chat_send.dto.g.dart';

@JsonSerializable()
class ChatSendDto extends BaseDto {
  int sender;
  String message_text;

  ChatSendDto({required this.sender, required this.message_text});

  factory ChatSendDto.fromJson(dynamic json) {
    return _$ChatSendDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.sender = serializable.sender;
    this.message_text = serializable.message_text;
  }

  @override
  ChatSendDto copy() => ChatSendDto(sender: this.sender, message_text: this.message_text)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$ChatSendDtoToJson(this);

}