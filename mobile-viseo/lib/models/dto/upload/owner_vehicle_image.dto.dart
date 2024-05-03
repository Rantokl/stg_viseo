import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'owner_vehicle_image.dto.g.dart';

@JsonSerializable()
class OwnerVehicleImgDto {
  int vehicle_id;
  int owner_id;

  OwnerVehicleImgDto({
    required this.vehicle_id,
    required this.owner_id,
  });

  factory OwnerVehicleImgDto.fromJson(dynamic json) {
    return _$OwnerVehicleImgDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.vehicle_id = serializable.vehicle_id;
    this.owner_id = serializable.owner_id;
  }

  @override
  OwnerVehicleImgDto copy() =>
      OwnerVehicleImgDto(vehicle_id: this.vehicle_id, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$OwnerVehicleImgDtoToJson(this);
}