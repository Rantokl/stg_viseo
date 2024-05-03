import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'mdp_oublier.dto.g.dart';

@JsonSerializable()
class MdpOublierDto {
  String to;
  int owner_id;

  MdpOublierDto({
    required this.to,
    required this.owner_id,
  });

  factory MdpOublierDto.fromJson(dynamic json) {
    return _$MdpOublierDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.to = serializable.to;
    this.owner_id = serializable.owner_id;
  }

  @override
  MdpOublierDto copy() =>
      MdpOublierDto(to: this.to, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$MdpOublierDtoToJson(this);
}