import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'date_actuelle.dto.g.dart';

/**
 * Cette est une definition d' heure envoyer par le back end
 */

@JsonSerializable()
class DateActuelleDto extends BaseDto {
  String date_actuelle;

  DateActuelleDto({required this.date_actuelle});

  factory DateActuelleDto.fromJson(dynamic json) {
    return _$DateActuelleDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.date_actuelle = serializable.date_actuelle;
  }

  @override
  DateActuelleDto copy() => DateActuelleDto(date_actuelle: this.date_actuelle)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$DateActuelleDtoToJson(this);

  @override
  String toString() {
    // TODO: implement toString
    return this.date_actuelle;
  }
}