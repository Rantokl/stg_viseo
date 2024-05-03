import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';

part 'mes_rdv.dto.g.dart';

@JsonSerializable()
class MesRdvDto extends BaseDto {
  int id_rdv;
  List<VehicleDto> vehicle;
  String type_rdv;
  String date_rdv;
  String heure_rdv;
  String number_vehicle;
  String status_rdv;
  String message;

  MesRdvDto({required this.id_rdv, required this.vehicle, required this.type_rdv, required this.date_rdv, required this.heure_rdv, required this.number_vehicle, required this.message, required this.status_rdv});

  factory MesRdvDto.fromJson(dynamic json) {
    return _$MesRdvDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.id_rdv = serializable.id_rdv;
    this.vehicle = serializable.vehicle;
    this.type_rdv = serializable.type_rdv;
    this.date_rdv = serializable.date_rdv;
    this.status_rdv = serializable.status_rdv;
    this.heure_rdv = serializable.heure_rdv;
    this.number_vehicle = serializable.number_vehicle;
    this.message = serializable.message;
  }

  @override
  MesRdvDto copy() => MesRdvDto(id_rdv: this.id_rdv, vehicle: this.vehicle, type_rdv: this.type_rdv, date_rdv: this.date_rdv, number_vehicle: this.number_vehicle, status_rdv: this.date_rdv, message: this.message, heure_rdv: this.heure_rdv)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$MesRdvDtoToJson(this);

}