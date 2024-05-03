import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'user.dto.g.dart';

@JsonSerializable()
class UserDto extends BaseDto {
  @JsonKey(name: "user_id")
  int id;
  String? name;
  String? token;
  String? refresh_token;
  int? room_id;

  UserDto({required this.id, required this.token, required this.refresh_token, this.room_id});

  factory UserDto.fromJson(dynamic json) {
    return _$UserDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.id = serializable.id;
    this.name = serializable.name;
    this.token = serializable.token;
    this.refresh_token = serializable.refresh_token;
    this.room_id = serializable.room_id;
  }

  @override
  UserDto copy() =>
      UserDto(id: this.id, token: this.token, refresh_token: this.refresh_token, room_id: this.room_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$UserDtoToJson(this);
}
