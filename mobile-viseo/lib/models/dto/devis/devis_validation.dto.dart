import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'devis_validation.dto.g.dart';

@JsonSerializable()
class DevisValidationdto extends BaseDto {
  int devis_id;
  String pdf;
  String status_devis;
  int owner_id;
  
  
  
  DevisValidationdto({required this.devis_id, required this.owner_id,required this.status_devis, required this.pdf});

  factory DevisValidationdto.fromJson(dynamic json) {
    return _$DevisValidationdtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.devis_id = serializable.devis_id;
    this.owner_id = serializable.owner_id;
    this.status_devis = serializable.status_devis;
    this.pdf = serializable.pdf;
  }

  @override
  DevisValidationdto copy() => DevisValidationdto(devis_id: this.devis_id, owner_id: this.owner_id, status_devis: this.status_devis, pdf: this.pdf)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$DevisValidationdtoToJson(this);

}