import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'etape_sav.dto.g.dart';

@JsonSerializable()
class EtapesavDto extends BaseDto {
  String etape;
  int status_id;
  String libelle;

  EtapesavDto({required this.etape, required this.status_id, required this.libelle});

  factory EtapesavDto.fromJson(dynamic json) {
    return _$EtapesavDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.etape = serializable.etape;
    this.status_id = serializable.status_id;
    this.libelle = serializable.libelle;
  }

  @override
  EtapesavDto copy() => EtapesavDto(etape: this.etape, status_id: this.status_id, libelle: this.libelle)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$EtapesavDtoToJson(this);

  String getStatus(int status_id) {
    if (status_id == 1) {
      return Assets.icons.dots;
    } else if (status_id == 2) {
      return Assets.icons.minus;
    }
    return Assets.icons.check;
  }

}