import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'panic.dto.g.dart';

@JsonSerializable()
class PanicDto extends BaseDto {
  int panique_id;
  String panique_menu;
  
  PanicDto({required this.panique_id, required this.panique_menu});

  factory PanicDto.fromJson(dynamic json) {
    return _$PanicDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.panique_id = serializable.panique_id;
    this.panique_menu = serializable.panique_menu;
  }

  @override
  PanicDto copy() => PanicDto(panique_id: this.panique_id, panique_menu: this.panique_menu)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$PanicDtoToJson(this);

}