import 'package:json_annotation/json_annotation.dart';

part 'vehicle.dto.g.dart';

@JsonSerializable()
class VehicleDto {
  int vehicle_id;
  String? number;
  String model;
  String? specification;
  String? image;
  int owner_id;

  VehicleDto({
    required this.vehicle_id,
    this.number,
    required this.model,
    this.specification,
    this.image,
    required this.owner_id,
  });

  factory VehicleDto.fromJson(dynamic json) {
    return _$VehicleDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.vehicle_id = serializable.vehicle_id;
    this.number = serializable.number;
    this.model = serializable.model;
    this.specification = serializable.specification;
    this.image = serializable.image;
    this.owner_id = serializable.owner_id;
  }

  @override
  VehicleDto copy() =>
      VehicleDto(vehicle_id: this.vehicle_id, number: this.number, model: this.model, specification: this.specification, image: this.image, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$VehicleDtoToJson(this);
}