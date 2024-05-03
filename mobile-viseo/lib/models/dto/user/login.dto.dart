import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'login.dto.g.dart';

@JsonSerializable()
class LoginDto {
  String username;
  String password;

  LoginDto({
    required this.username,
    required this.password,
  });

  factory LoginDto.fromJson(dynamic json) {
    return _$LoginDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.username = serializable.username;
    this.password = serializable.password;
  }

  @override
  LoginDto copy() =>
      LoginDto(username: this.username, password: this.password)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$LoginDtoToJson(this);
}