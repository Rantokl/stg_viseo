import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/rdv/date_actuelle_response.dto.dart';
import 'package:sav/models/dto/rdv/heure_prise_rdv_response.dto.dart';
import 'package:sav/models/dto/rdv/mes_rdv_response.dto.dart';
import 'package:sav/models/dto/rdv/prise_rdv.dto.dart';
import 'package:sav/models/dto/rdv/prise_rdv_response.dto.dart';
import 'package:sav/models/dto/rdv/type_date_rdv.dto.dart';
import 'package:sav/models/dto/rdv/type_rdv_response.dto.dart';
import 'package:sav/repository/remote/rdv/rdv_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

class RdvRemoteSA extends BaseRemoteSA{
  final rdvRepository = RdvRemoteRepo();

  // Prise rdv
  postPriseRdv ({
    required int vehicleId,
    required PriseRdvDto priseRdvDto,
    required CompletionClosure<PriseRdvResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await rdvRepository.postPriseRdv(priseRdvDto, vehicleId);
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }

  updateRdv ({
    required int vehicleId,
    required int rdvId,
    required PriseRdvDto priseRdvDto,
    required CompletionClosure<PriseRdvResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await rdvRepository.updateRdv(priseRdvDto, vehicleId, rdvId);
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }


  getTypeRdv({
    required CompletionClosure<TypeRdvResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await rdvRepository.getTypeRdv();
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }

  // Mes rdv
  getMesRdv({
    required CompletionClosure<MesRdvResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await rdvRepository.getMesRdv();
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }


  getHeurePriseRdv({
    required int type_rendez_vous_id,
    required String date_rendez_vous,
    required CompletionClosure<HeurePriseRdvResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    TypeDateRdvDto typeDateRdv = TypeDateRdvDto(type_rendez_vous_id: type_rendez_vous_id, date_rendez_vous: date_rendez_vous);
    var response = await rdvRepository.getHeurePriseRdv(typeDateRdv);
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

  getDateActuel({
    required CompletionClosure<DateActuelleResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
     var response = await rdvRepository.getDateActuelle();
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