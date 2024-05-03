import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'user_logout.dto.g.dart';

@JsonSerializable()
class UserLogoutDto extends BaseDto {
  int user_id;
  
  UserLogoutDto({required this.user_id});

  factory UserLogoutDto.fromJson(dynamic json) {
    return _$UserLogoutDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.user_id = serializable.user_id;
  }

  @override
  UserLogoutDto copy() => UserLogoutDto(user_id: this.user_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$UserLogoutDtoToJson(this);

}