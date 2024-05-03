
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/livraison/check_list_item/list_checkListLivraison.dto.dart';
import 'package:sav/models/dto/livraison/check_list_livraison/check_list_livraison_response.dto.dart';
import 'package:sav/repository/remote/livraison/livraison_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

class LivraisonRemoteSA extends BaseRemoteSA{
  final livraisonRepository = LivraisonRemoteRepo();

  getCheckListLivraisonByVehicle({
    required int idVehicle,
    required CompletionClosure<CheckListLivraisonResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure,
    
  }) async {
    var response = await livraisonRepository.getOptionListLivraisonByVehicle(idVehicle);
    switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }

  getCheckListLivraison({
    required CompletionClosure<CheckListLivraisonResponseDto> onSuccess,
    CompletionClosure<String>? onFailure,
    
  }) async {
    var response = await livraisonRepository.getOptionListLivraison();
    switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

  postCheckListLivraison({
    required ListCheckListLivraison listCheckListLivraison,
    required int vehicle_id,
    required CompletionClosure<BaseResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    print(listCheckListLivraison.toJsonLocal());
    var response = await livraisonRepository.postCheckListItems(listCheckListLivraison, vehicle_id);
    switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }
}