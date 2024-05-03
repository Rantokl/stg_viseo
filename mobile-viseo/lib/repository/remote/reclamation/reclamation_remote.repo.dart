import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/reclamation/reclamation_client.dto.dart';
import 'package:sav/models/dto/reclamation/reclamation_client_response.dto.dart';
import 'package:sav/models/dto/reclamation/type_reclamation_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class ReclamationRemoteRepo{
  BaseRemoteBDL get _helper => BaseRemoteBDL();

  // Reclamation client
  Future<ReclamationClientResponseDto> postReclamationClient(ReclamationClientDto reclamationClientDto, int vehicleId) async {
    var response = await _helper.post(
      "${Urls.reclamation.reclamationClient}/$vehicleId/",
      body: reclamationClientDto.toJsonLocal(),
    );
    return ReclamationClientResponseDto.fromJson(response);
  }

  Future<TypeReclamationResponseDto> getTypeReclamation() async {
    var response = await _helper.get(
      "${Urls.reclamation.typeReclamation}",
    );
    return TypeReclamationResponseDto.fromJson(response);
  }

}