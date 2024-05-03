import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/garantie/carnet_garantie_response.dto.dart';
import 'package:sav/repository/remote/garantie/garantie_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

class GarantieRemoteSA extends BaseRemoteSA{
  final garantieRepository = GarantieRemoteRepo();

  getCarnetGarantie({
    required int vehicleId,
    required CompletionClosure<CarnetGarantieResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await garantieRepository.getCarnetGarantie(vehicleId);
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