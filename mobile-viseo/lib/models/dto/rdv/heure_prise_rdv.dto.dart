import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'heure_prise_rdv.dto.g.dart';

@JsonSerializable()
class HeurePriseRdvDto extends BaseDto {
  String date_rendez_vous;
  String heure_rendez_vous;

  HeurePriseRdvDto({required this.date_rendez_vous, required this.heure_rendez_vous});

  factory HeurePriseRdvDto.fromJson(dynamic json) {
    return _$HeurePriseRdvDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.date_rendez_vous = serializable.date_rendez_vous;
    this.heure_rendez_vous = serializable.heure_rendez_vous;
  }

  @override
  HeurePriseRdvDto copy() => HeurePriseRdvDto(date_rendez_vous: this.date_rendez_vous, heure_rendez_vous: this.heure_rendez_vous)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$HeurePriseRdvDtoToJson(this);

}
