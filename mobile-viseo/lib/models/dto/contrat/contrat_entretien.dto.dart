import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'contrat_entretien.dto.g.dart';

@JsonSerializable()
class ContratEntretienDto extends BaseDto {
  int vehicle_id;
  String pdf;
  int owner_id;


  ContratEntretienDto({required this.vehicle_id, required this.pdf, required this.owner_id});

  factory ContratEntretienDto.fromJson(dynamic json) {
    return _$ContratEntretienDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.vehicle_id = serializable.vehicle_id;
    this.pdf = serializable.pdf;
    this.owner_id = serializable.owner_id;
  }

  @override
  ContratEntretienDto copy() => ContratEntretienDto(vehicle_id: this.vehicle_id, pdf: this.pdf, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$ContratEntretienDtoToJson(this);

}