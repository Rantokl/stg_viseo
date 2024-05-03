import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'menu.dto.g.dart';

@JsonSerializable()
class MenuDto extends BaseDto {
  int menu_id;
  String menu;
  
  MenuDto({required this.menu_id, required this.menu});

  factory MenuDto.fromJson(dynamic json) {
    return _$MenuDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.menu_id = serializable.menu_id;
    this.menu = serializable.menu;
  }

  @override
  MenuDto copy() => MenuDto(menu_id: this.menu_id, menu: this.menu)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$MenuDtoToJson(this);
}