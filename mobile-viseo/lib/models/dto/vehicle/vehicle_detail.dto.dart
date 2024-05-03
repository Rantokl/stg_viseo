import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/menu/menu.dto.dart';

part 'vehicle_detail.dto.g.dart';

@JsonSerializable()
class VehicleDetailDto extends BaseDto{
  int vehicle_id;
  String? number;
  String model;
  String? specification;
  String? image;
  int owner_id;
  List<MenuDto> menus;

  VehicleDetailDto({
    required this.vehicle_id,
    this.number,
    required this.model,
    this.specification,
    this.image,
    required this.owner_id,
    required this.menus
  });

  factory VehicleDetailDto.fromJson(dynamic json) {
    return _$VehicleDetailDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.vehicle_id = serializable.vehicleId;
    this.number = serializable.number;
    this.model = serializable.model;
    this.specification = serializable.specification;
    this.image = serializable.image;
    this.owner_id = serializable.ownerId;
    this.menus = serializable.menus;
  }

  @override
  VehicleDetailDto copy() =>
    VehicleDetailDto(vehicle_id: this.vehicle_id, number: this.number,
        model: this.model, specification: this.specification,
        image: this.image, owner_id: this.owner_id, menus: this.menus)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$VehicleDetailDtoToJson(this);
}