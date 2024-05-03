import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'demande_devis.dto.g.dart';

@JsonSerializable()
class demandeDevisDto extends BaseDto {
  int type_devis_id;
  String details;
  String? pdf;
  String? prix;
  String? resume;
  String? numero_devis;
  
  demandeDevisDto({required this.type_devis_id, required this.details, this.pdf, this.prix, this.resume, this.numero_devis});

  factory demandeDevisDto.fromJson(dynamic json) {
    return _$demandeDevisDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.type_devis_id = serializable.type_devis_id;
    this.details = serializable.details;
    this.pdf = serializable.pdf;
    this.prix = serializable.prix;
    this.resume = serializable.resume;
    this.numero_devis = serializable.numero_devis;
  }

  @override
  demandeDevisDto copy() => demandeDevisDto(type_devis_id: this.type_devis_id, details: this.details, pdf: this.pdf, prix: this.prix, resume: this.resume, numero_devis: this.numero_devis)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$demandeDevisDtoToJson(this);
}