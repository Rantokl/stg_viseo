import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/vehicle/vehicle_detail_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class VehicleDetailRemoteRepo{
  BaseRemoteBDL get _helper => BaseRemoteBDL();

  Future<VehicleDetailResponseDto> getVehicleDetail(int id) async {
    var response = await _helper.get(
      "${Urls.vehicle.detail}/$id",
    );
    
    return VehicleDetailResponseDto.fromJson(response);
  }
}