import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/contrat/contrat_entretien_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class ContratRemoteRepo{
  BaseRemoteBDL get _helper => BaseRemoteBDL();

  Future<ContratEntretienResponseDto> getContratEntretien(int vehicleId) async {
    var response = await _helper.get(
      "${Urls.contrat.contratEntretien}/$vehicleId/",
    );

    return ContratEntretienResponseDto.fromJson(response);
  }

}