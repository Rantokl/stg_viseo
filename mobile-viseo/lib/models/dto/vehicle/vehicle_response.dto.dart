

import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';


class VehiculeResponseDto extends BaseResponseDto {
  late List<VehicleDto> data = [];
  VehiculeResponseDto() : super();

  VehiculeResponseDto.fromJson(Map<String, dynamic> json)
        : super.fromJson(json) {
        var jsonData = getData(json);
        if ((json != null) && (jsonData != null)) {
            this.data = (jsonData as List<dynamic>)
                .map((item) => VehicleDto.fromJson(item))
                .toList();
        }
    }
}