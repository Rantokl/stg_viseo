import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'contact.dto.g.dart';

@JsonSerializable()
class ContactDto extends BaseDto {
  String? nom;
  @JsonKey(name: "téléphone")
  String? telephone;
  @JsonKey(name: "siège")
  String? siege;
  String type_contact_id;


  ContactDto({this.nom, this.telephone, this.siege, required this.type_contact_id});

  factory ContactDto.fromJson(dynamic json) {
    return _$ContactDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.nom = serializable.nom;
    this.telephone = serializable.telephone;
    this.siege = serializable.siege;
    this.type_contact_id = serializable.type_contact_id;
  }

  @override
  ContactDto copy() => ContactDto(nom: this.nom, telephone: this.telephone, siege: this.siege, type_contact_id: this.type_contact_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$ContactDtoToJson(this);

}