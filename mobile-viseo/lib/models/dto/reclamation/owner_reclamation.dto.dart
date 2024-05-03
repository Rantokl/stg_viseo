import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'owner_reclamation.dto.g.dart';

@JsonSerializable()
class OwnerReclamationDto extends BaseDto {
  String message;
  int vehicle_id;
  int reclamation_id;
  int owner_id;

  OwnerReclamationDto({required this.message, required this.vehicle_id, required this.reclamation_id, required this.owner_id});

  factory OwnerReclamationDto.fromJson(dynamic json) {
    return _$OwnerReclamationDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.message = serializable.message;
    this.vehicle_id = serializable.vehicle_id;
    this.reclamation_id = serializable.reclamation_id;
    this.owner_id = serializable.owner_id;
  }

  @override
  OwnerReclamationDto copy() => OwnerReclamationDto(message: this.message, vehicle_id: this.vehicle_id, reclamation_id: this.reclamation_id, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$OwnerReclamationDtoToJson(this);
}