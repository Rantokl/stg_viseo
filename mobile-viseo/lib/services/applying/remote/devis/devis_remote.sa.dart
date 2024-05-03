import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/devis/demande_devis.dto.dart';
import 'package:sav/models/dto/devis/demande_devis_response.dto.dart';
import 'package:sav/models/dto/devis/type_devis_response.dto.dart';
import 'package:sav/repository/remote/devis/devis_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';
import 'package:sav/models/dto/devis/devis_commentaire.dto.dart';
import 'package:sav/models/dto/devis/devis_commentaire_response.dto.dart';
import 'package:sav/models/dto/devis/devis_validation_response.dto.dart';
import 'package:sav/models/dto/devis/list_devis_response.dto.dart';

class DevisRemoteSA extends BaseRemoteSA {

  final repository = DevisRemoteRepo();

  getTypeDevis ({
    required CompletionClosure<TypeDevisResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
     var response = await repository.getTypeDevis();
     switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }

  postDemandeDevis ({
    required int vehicle_id,
    required demandeDevisDto request,
    required CompletionClosure<DemandeDevisResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await repository.postDemandeDevis(request, vehicle_id);
     switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }

  getListDevis({
    required int id,
    required CompletionClosure<ListDevisResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await repository.getListDevis(id);
    switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }

  devisValidation({
    required int id,
    required int validation,
    required CompletionClosure<DevisValidationResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await repository.validationDevis(id, validation);
    switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }

   devisCommentaire ({
    required int id,
    required DevisCommentaire request,
    required CompletionClosure<DevisCommentaireResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await repository.devisCommentaire(id, request);
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