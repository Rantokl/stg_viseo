import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/chat/message.dto.dart';

part 'owner_chat.dto.g.dart';

@JsonSerializable()
class OwnerChatDto extends BaseDto {
  int room_id;
  int message_id;

  OwnerChatDto({required this.room_id, required this.message_id});

  factory OwnerChatDto.fromJson(dynamic json) {
    return _$OwnerChatDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.room_id = serializable.room_id;
    this.message_id = serializable.message_id;
  }

  @override
  OwnerChatDto copy() => OwnerChatDto(room_id: this.room_id, message_id: this.message_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$OwnerChatDtoToJson(this);
}