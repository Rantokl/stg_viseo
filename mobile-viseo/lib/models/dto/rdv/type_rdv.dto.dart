import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'type_rdv.dto.g.dart';

@JsonSerializable()
class TypeRdvDto extends BaseDto {
  int id;
  String libelle;

  TypeRdvDto({required this.id, required this.libelle});

  factory TypeRdvDto.fromJson(dynamic json) {
    return _$TypeRdvDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.id = serializable.id;
    this.libelle = serializable.libelle;
  }

  @override
  TypeRdvDto copy() => TypeRdvDto(id: this.id, libelle: this.libelle)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$TypeRdvDtoToJson(this);

  @override
  String toString() {
    return this.libelle;
  }
}