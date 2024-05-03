import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/sav/etape_sav.dto.dart'; // Assurez-vous que le chemin vers EtapesavDto est correct

part 'sav.dto.g.dart';

@JsonSerializable()
class SavDto extends BaseDto {
  int id;
  String reference;
  String type_sav;
  int status_sav_id;
  String libelle_status_sav;
  String date_sav;
  int vehicle_id;
  int owner_id;
  List<EtapesavDto> etape_sav; // Ajout de EtapesavDto

  SavDto({
    required this.id,
    required this.reference,
    required this.type_sav,
    required this.status_sav_id,
    required this.libelle_status_sav,
    required this.date_sav,
    required this.vehicle_id,
    required this.owner_id,
    required this.etape_sav, // Initialisation de EtapesavDto
  });

  factory SavDto.fromJson(dynamic json) {
    return _$SavDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.id = serializable.id;
    this.reference = serializable.reference;
    this.type_sav = serializable.type_sav;
    this.status_sav_id = serializable.status_sav_id;
    this.libelle_status_sav = serializable.libelle_status_sav;
    this.date_sav = serializable.date_sav;
    this.vehicle_id = serializable.vehicle_id;
    this.owner_id = serializable.owner_id;
    this.etape_sav = serializable.etape_sav; // Attribution de EtapesavDto
  }

  @override
  SavDto copy() => SavDto(
        id: this.id,
        reference: this.reference,
        type_sav: this.type_sav,
        status_sav_id: this.status_sav_id,
        libelle_status_sav: this.libelle_status_sav,
        date_sav: this.date_sav,
        vehicle_id: this.vehicle_id,
        owner_id: this.owner_id,
        etape_sav: this.etape_sav, // Copie de EtapesavDto
      );

  @override
  Map<String, dynamic> toJsonLocal() => _$SavDtoToJson(this);
}
