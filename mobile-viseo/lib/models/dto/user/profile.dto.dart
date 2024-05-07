import 'package:json_annotation/json_annotation.dart';

part 'profile.dto.g.dart';

@JsonSerializable()
class ProfileDto {
  String? mobile;
  String? email;
  String? first_name;
  String username;
  bool isAdmin;
  int owner_id;

  ProfileDto({
    this.mobile,
    this.email,
    this.first_name,
    required this.username,
    required this.isAdmin,
    required this.owner_id,
    
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
    this.first_name = serializable.first_name;
  }

  @override
  ProfileDto copy() =>
      ProfileDto(mobile: this.mobile, email: this.email, username: this.username, isAdmin: this.isAdmin, owner_id: this.owner_id, first_name: this.first_name)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$ProfileDtoToJson(this);
}