import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'prise_rdv.dto.g.dart';

@JsonSerializable()
class PriseRdvDto extends BaseDto {
  int type_rendez_vous_id;
  String date_rendez_vous;
  String heure_rendez_vous;
  String message;

  PriseRdvDto({required this.type_rendez_vous_id, required this.date_rendez_vous, required this.heure_rendez_vous, required this.message});

  factory PriseRdvDto.fromJson(dynamic json) {
    return _$PriseRdvDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.type_rendez_vous_id = serializable.type_rendez_vous_id;
    this.date_rendez_vous = serializable.date_rendez_vous;
    this.heure_rendez_vous = serializable.heure_rendez_vous;
    this.message = serializable.message;
  }

  @override
  PriseRdvDto copy() => PriseRdvDto(type_rendez_vous_id: this.type_rendez_vous_id, date_rendez_vous: this.date_rendez_vous, heure_rendez_vous: this.heure_rendez_vous, message: this.message)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$PriseRdvDtoToJson(this);

}
