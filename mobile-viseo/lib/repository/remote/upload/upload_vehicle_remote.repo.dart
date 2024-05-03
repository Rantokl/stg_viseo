import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/upload/upload_vehicle.dto.dart';
import 'package:sav/models/dto/upload/upload_vehicle_response.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle_detail_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class UploadVehicleRemoteRepo{
  BaseRemoteBDL get _helper => BaseRemoteBDL();

  Future<UploadVehicleResponseDto> uploadVehicle(UploadVehicleDto vehicle, int id) async {

    final appCacheDir = await getTemporaryDirectory();
    FormData formData = FormData.fromMap({
        "image": await MultipartFile.fromFile('${vehicle.image}'),
    });
    var response = await _helper.postFormData(
      "${Urls.uploadVehicle.upload}/$id/",
      formData
    );
    
    return UploadVehicleResponseDto.fromJson(response);
  }
}