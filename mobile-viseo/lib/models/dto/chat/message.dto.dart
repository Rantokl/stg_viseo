import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'message.dto.g.dart';

@JsonSerializable()
class MessageDto extends BaseDto {
  int sender;
  String message_text;
  String time;

  MessageDto({required this.sender, required this.message_text, required this.time});

  factory MessageDto.fromJson(dynamic json) {
    return _$MessageDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.sender = serializable.sender;
    this.message_text = serializable.message_text;
    this.time = serializable.time;
  }

  @override
  MessageDto copy() => MessageDto(sender: this.sender, message_text: this.message_text, time: this.time)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$MessageDtoToJson(this);
}