import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/garantie/carnet_garantie_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class GarantieRemoteRepo{
  BaseRemoteBDL get _helper => BaseRemoteBDL();

  Future<CarnetGarantieResponseDto> getCarnetGarantie(int vehicleId) async {
    var response = await _helper.get(
      "${Urls.garantie.carnetGarantie}/$vehicleId/",
    );

    return CarnetGarantieResponseDto.fromJson(response);
  }

}