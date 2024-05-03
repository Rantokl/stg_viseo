import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'type_date_rdv.dto.g.dart';

@JsonSerializable()
class TypeDateRdvDto extends BaseDto {
  int type_rendez_vous_id;
  String date_rendez_vous;

  TypeDateRdvDto({required this.type_rendez_vous_id, required this.date_rendez_vous});
  
  @override
  bind(serializable) {
    this.type_rendez_vous_id = serializable.type_rendez_vous_id;
    this.date_rendez_vous = serializable.date_rendez_vous;
  }
  
  @override
  TypeDateRdvDto copy() => TypeDateRdvDto(type_rendez_vous_id: this.type_rendez_vous_id, date_rendez_vous: this.date_rendez_vous);
  
  @override
  Map<String, dynamic> toJsonLocal() => _$TypeDateRdvDtoToJson(this);

}