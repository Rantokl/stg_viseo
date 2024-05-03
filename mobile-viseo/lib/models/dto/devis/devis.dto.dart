import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'devis.dto.g.dart';

@JsonSerializable()
class DevisDto extends BaseDto {
  int devis_id;
  String type_devis;
  String? numero_devis;
  String? prix;
  String? resume;
  String details;
  String date_devis;
  String? date_upload_devis;
  String status_devis;
  String? pdf;
  int owner_id;
  
  DevisDto({required this.devis_id, required this.type_devis, this.numero_devis, this.prix, this.resume, required this.details,this.date_upload_devis, required this.date_devis,required this.status_devis, this.pdf, required this.owner_id});

  factory DevisDto.fromJson(dynamic json) {
    return _$DevisDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.devis_id = serializable.devis_id;
    this.type_devis = serializable.type_devis;
    this.numero_devis = serializable.numero_devis;
    this.prix = serializable.prix;
    this.resume = serializable.resume;
    this.details = serializable.details;
    this.date_upload_devis = serializable.date_upload_devis;
    this.date_devis = serializable.date_devis;
    this.status_devis = serializable.status_devis;
    this.pdf = serializable.pdf;
    this.owner_id = serializable.owner_id;
  }

  @override
  DevisDto copy() => DevisDto(devis_id: this.devis_id, type_devis: this.type_devis, numero_devis: this.numero_devis, prix: this.prix, resume: this.resume, details: this.details, date_devis: this.date_devis, date_upload_devis: this.date_upload_devis, status_devis: this.status_devis, pdf: this.pdf, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$DevisDtoToJson(this);

}