import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'email.dto.g.dart';

@JsonSerializable()
class EmailDto {
  String from_user;

  EmailDto({
    required this.from_user,
  });

  factory EmailDto.fromJson(dynamic json) {
    return _$EmailDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.from_user = serializable.from_user;
  }

  @override
  EmailDto copy() =>
      EmailDto(from_user: this.from_user)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$EmailDtoToJson(this);
}