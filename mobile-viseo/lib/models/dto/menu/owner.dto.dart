import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'owner.dto.g.dart';

@JsonSerializable()
class OwnerDto extends BaseDto {
  int vehicle_id;
  int owner_id;
  
  OwnerDto({required this.vehicle_id, required this.owner_id});

  factory OwnerDto.fromJson(dynamic json) {
    return _$OwnerDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.vehicle_id = serializable.vehicle_id;
    this.owner_id = serializable.owner_id;
  }

  @override
  OwnerDto copy() => OwnerDto(vehicle_id: this.vehicle_id, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$OwnerDtoToJson(this);
}