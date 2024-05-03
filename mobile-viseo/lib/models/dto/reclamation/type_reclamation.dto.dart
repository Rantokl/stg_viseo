import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'type_reclamation.dto.g.dart';

@JsonSerializable()
class TypeReclamationDto extends BaseDto {
  int id;
  String libelle;

  TypeReclamationDto({required this.id, required this.libelle});

  factory TypeReclamationDto.fromJson(dynamic json) {
    return _$TypeReclamationDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.id = serializable.id;
    this.libelle = serializable.libelle;
  }

  @override
  TypeReclamationDto copy() => TypeReclamationDto(id: this.id, libelle: this.libelle)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$TypeReclamationDtoToJson(this);

  @override
  String toString() {
    return this.libelle;
  }
}