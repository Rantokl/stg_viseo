

import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';


class SearchVehiculeResponseDto extends BaseResponseDto {
  VehicleDto? data = null ;
  SearchVehiculeResponseDto() : super();

  SearchVehiculeResponseDto.fromJson(dynamic json)
        : super.fromJson(json) {
        var jsonData = getData(json);
        if ((json != null) && (jsonData != null)) {
            this.data = VehicleDto.fromJson(jsonData);
        }
    }
}