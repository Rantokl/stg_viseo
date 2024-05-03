

import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/vehicle/search_vehicule_response.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class VehiculeRemoteRepo {
  BaseRemoteBDL get helper => BaseRemoteBDL();
  
 Future<VehiculeResponseDto> getUserCar (int id) async {
    var response = await helper.get(
      "${Urls.vehicle.list}/" ,
    );
    return VehiculeResponseDto.fromJson(response);
  }

 Future<VehiculeResponseDto> getSearchCar (String number) async {
    var response = await helper.get(
      "${Urls.vehicle.search}/${number.toUpperCase()}/" ,
    );
    return VehiculeResponseDto.fromJson(response);
  }
}