import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'fbm.dto.g.dart';

@JsonSerializable()
class FbmDto extends BaseDto {
  String fbm;
  int owner_id;
  
  FbmDto({required this.fbm, required this.owner_id});

  factory FbmDto.fromJson(dynamic json) {
    return _$FbmDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.fbm = serializable.fbm;
    this.owner_id = serializable.owner_id;
  }

  @override
  FbmDto copy() => FbmDto(fbm: this.fbm, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$FbmDtoToJson(this);

}