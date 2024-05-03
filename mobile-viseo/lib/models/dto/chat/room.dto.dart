import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/chat/message.dto.dart';

part 'room.dto.g.dart';

@JsonSerializable()
class RoomDto extends BaseDto{
  int room_id;
  List<MessageDto> messages;
  int client_id;


  RoomDto({
    required this.room_id,
    required this.messages,
    required this.client_id
  });

  factory RoomDto.fromJson(dynamic json) {
    return _$RoomDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.room_id = serializable.room_id;
    this.messages = serializable.messages;
    this.client_id = serializable.client_id;
  }

  @override
  RoomDto copy() =>
      RoomDto(room_id: this.room_id, messages: this.messages, client_id: this.client_id,)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$RoomDtoToJson(this);
}