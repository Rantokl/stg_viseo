import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle_detail.dto.dart';

class VehicleDetailResponseDto extends BaseResponseDto {
  late VehicleDetailDto data;

  VehicleDetailResponseDto():super();

  VehicleDetailResponseDto.fromJson(dynamic json) : super.fromJson(json) {
    var jsonData = getData(json);
    if ((json != null) && (jsonData != null)) {
      this.data = VehicleDetailDto.fromJson(jsonData);
    }
  }
}