import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/reclamation/reclamation_client.dto.dart';
import 'package:sav/models/dto/reclamation/reclamation_client_response.dto.dart';
import 'package:sav/models/dto/reclamation/type_reclamation_response.dto.dart';
import 'package:sav/repository/remote/reclamation/reclamation_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

class ReclamationRemoteSA extends BaseRemoteSA{
  final reclamationRepository = ReclamationRemoteRepo();

  // Reclamation client
  postReclamationClient ({
    required int vehicleId,
    required ReclamationClientDto reclamationClientDto,
    required CompletionClosure<ReclamationClientResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await reclamationRepository.postReclamationClient(reclamationClientDto, vehicleId);
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }

  getTypeReclamation({
    required CompletionClosure<TypeReclamationResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await reclamationRepository.getTypeReclamation();
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }
}