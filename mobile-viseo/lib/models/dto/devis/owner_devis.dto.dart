import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'owner_devis.dto.g.dart';

@JsonSerializable()
class OwnerDevisDto extends BaseDto {
  int vehicle_id;
  int owner_id;
  int status_id;
  int devis_id;
  
  OwnerDevisDto({required this.vehicle_id, required this.owner_id, required this.status_id, required this.devis_id});

  factory OwnerDevisDto.fromJson(dynamic json) {
    return _$OwnerDevisDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.vehicle_id = serializable.vehicle_id;
    this.owner_id = serializable.owner_id;
    this.status_id = serializable.status_id;
    this.devis_id = serializable.devis_id;
  }

  @override
  OwnerDevisDto copy() => OwnerDevisDto(vehicle_id: this.vehicle_id, owner_id: this.owner_id, status_id: this.status_id, devis_id: this.devis_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$OwnerDevisDtoToJson(this);
}