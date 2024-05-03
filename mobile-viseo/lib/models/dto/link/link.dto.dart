import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'link.dto.g.dart';

@JsonSerializable()
class LinkDto extends BaseDto {
  String link;
  
  LinkDto({required this.link});

  factory LinkDto.fromJson(dynamic json) {
    return _$LinkDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.link = serializable.link;
  }

  @override
  LinkDto copy() => LinkDto(link: this.link)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$LinkDtoToJson(this);

}