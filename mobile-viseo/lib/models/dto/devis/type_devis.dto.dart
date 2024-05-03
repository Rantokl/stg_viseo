import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'type_devis.dto.g.dart';

@JsonSerializable()
class TypeDevisDto extends BaseDto {
  int id;
  String libelle;
  
  TypeDevisDto({required this.id, required this.libelle});

  factory TypeDevisDto.fromJson(dynamic json) {
    return _$TypeDevisDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.id = serializable.id;
    this.libelle = serializable.libelle;
  }

  @override
  TypeDevisDto copy() => TypeDevisDto(id: this.id, libelle: this.libelle)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$TypeDevisDtoToJson(this);

  @override
  String toString() {
    // TODO: implement toString
    return libelle;
  }
}