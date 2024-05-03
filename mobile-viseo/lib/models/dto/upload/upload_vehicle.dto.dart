import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'upload_vehicle.dto.g.dart';

@JsonSerializable()
class UploadVehicleDto {
  String image;

  UploadVehicleDto({
    required this.image,
  });

  factory UploadVehicleDto.fromJson(dynamic json) {
    return _$UploadVehicleDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.image = serializable.image;
  }

  @override
  UploadVehicleDto copy() =>
      UploadVehicleDto(image: this.image)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$UploadVehicleDtoToJson(this);
}