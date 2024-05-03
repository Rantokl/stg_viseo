import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/contrat/contrat_entretien_response.dto.dart';
import 'package:sav/repository/remote/contrat/contrat_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

class ContratRemoteSA extends BaseRemoteSA{
  final contratRepo = ContratRemoteRepo();

  getContratEntretien({
    required int vehicleId,
    required CompletionClosure<ContratEntretienResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await contratRepo.getContratEntretien(vehicleId);
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