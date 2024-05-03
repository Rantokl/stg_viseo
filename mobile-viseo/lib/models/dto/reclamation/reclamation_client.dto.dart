import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'reclamation_client.dto.g.dart';

@JsonSerializable()
class ReclamationClientDto extends BaseDto {
  int type_reclamation_id;
  String message;

  ReclamationClientDto({required this.type_reclamation_id,required this.message});

  factory ReclamationClientDto.fromJson(dynamic json) {
    return _$ReclamationClientDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.type_reclamation_id = serializable.type_reclamation_id;
    this.message = serializable.message;
  }

  @override
  ReclamationClientDto copy() => ReclamationClientDto(type_reclamation_id: this.type_reclamation_id, message: this.message)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$ReclamationClientDtoToJson(this);

}