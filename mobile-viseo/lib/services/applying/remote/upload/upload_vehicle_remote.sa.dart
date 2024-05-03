import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/upload/upload_vehicle.dto.dart';
import 'package:sav/models/dto/upload/upload_vehicle_response.dto.dart';
import 'package:sav/repository/remote/upload/upload_vehicle_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

class UploadVehicleRemoteSA extends BaseRemoteSA{
  final uploadVehicleRemoteRepo = UploadVehicleRemoteRepo();

  uploadVehicle ({
    required int vehicleId,
    required UploadVehicleDto vehicle,
    required CompletionClosure<UploadVehicleResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await uploadVehicleRemoteRepo.uploadVehicle(vehicle, vehicleId);
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }
}