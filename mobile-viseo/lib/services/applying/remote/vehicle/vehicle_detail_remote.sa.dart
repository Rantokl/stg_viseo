import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle_detail_response.dto.dart';
import 'package:sav/repository/remote/vehicle/vehicle_detail_remote.repo.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

class VehicleDetailRemoteSA extends BaseRemoteSA{
  final vehicleRepository = VehicleDetailRemoteRepo();

  getVehicleDetail({
    required int id,
    required CompletionClosure<VehicleDetailResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await vehicleRepository.getVehicleDetail(id);
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