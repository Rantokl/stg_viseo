import 'package:json_annotation/json_annotation.dart';

part 'profile.dto.g.dart';

@JsonSerializable()
class ProfileDto {
  String? mobile;
  String? email;
  String username;
  String firstname;
  bool isAdmin;
  int owner_id;

  ProfileDto({
    this.mobile,
    this.email,
    required this.username,
    required this.isAdmin,
    required this.owner_id,
    this.firstname,
  });

  factory ProfileDto.fromJson(dynamic json) {
    return _$ProfileDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.mobile = serializable.mobile;
    this.email = serializable.email;
    this.username = serializable.username;
    this.isAdmin = serializable.isAdmin;
    this.owner_id = serializable.owner_id;
    this.firstname = serializable.firstname;
  }

  @override
  ProfileDto copy() =>
      ProfileDto(mobile: this.mobile, email: this.email, username: this.username, isAdmin: this.isAdmin, owner_id: this.owner_id, firstname: this.firstname)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$ProfileDtoToJson(this);
}