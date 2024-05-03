import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:get/get_rx/src/rx_types/rx_types.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/dto/livraison/check_list_item/checkListItem.dto.dart';
import 'package:sav/models/dto/livraison/check_list_item/list_checkListLivraison.dto.dart';
import 'package:sav/models/dto/livraison/check_list_livraison/check_list_livraison_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';
import 'package:sav/services/applying/remote/livraison/livraison_remote.sa.dart';

import '../../../models/constant/values/strings.dart';
import '../../../models/dto/base_response.dto.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class LivraisonCheckListController extends BaseController {
  LivraisonCheckListController() : super();
  late List<CheckListItemDto> listCheckListItemDto;
  late LivraisonRemoteSA service;
  late Rx<CheckListLivraisonResponseDto?> checkListLivraison = Rx<CheckListLivraisonResponseDto?>(null);
  RxBool isTokenExpired = false.obs;
  
  @override
  onInit() {
    super.onInit();
    this.service = LivraisonRemoteSA();
    listCheckListItemDto = [];
  }

  @override
  void onReady() {
    super.onReady();
  }

  getCheckListLivraison(
  {
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
}
      ) async {
    loading(true);
    await service.getCheckListLivraisonByVehicle(
      idVehicle: vehicleSelected!.vehicle_id,
      onSuccess: (response) {
        checkListLivraison.value = response;
        loading(false);
        success.call(true);
      },
      onFailure: (response){
        if (response.statusCode == Strings.common.expiredTokenCode){
          UserRemoteSA().logout();
          isTokenExpired.value = true;
          loading(false);
          failure?.call(response);
        }
        else{
          service.getCheckListLivraison(onSuccess: (response){
            checkListLivraison.value = response;
            loading(false);
          },
              onFailure: (error){
                loading(false);
              }
          );
        }
      }
    );
  }

  changeCheckItem(int item_id, int id){
    checkListLivraison.value?.data.forEach((item){
      if(item.items_id == item_id){
        item.details.forEach((detail){
          if(detail.id == id){
            detail.isChecked = !detail.isChecked;
          }
        });
      }
    });
    checkListLivraison.refresh();
  }

  Future<List<CheckListItemDto>> listCheckListItemDto_extract() async{
     checkListLivraison.value?.data.forEach((item){
      item.details.forEach((detail){
        listCheckListItemDto.add(CheckListItemDto(items_id: item.items_id, details_id : detail.id, status: detail.isChecked?? false));
      });
    });
    return listCheckListItemDto;
  }

  postCheckListItems({
    required int stateId,
    required CompletionClosure<String> success,
    CompletionClosure<BaseResponseDto>? failure
  }) async {
    await listCheckListItemDto_extract();
    ListCheckListLivraison listCheckListLivraison = ListCheckListLivraison(items: listCheckListItemDto, commentaire: "", stateId: stateId);
    loading(true);
    await this.service.postCheckListLivraison(
      listCheckListLivraison : listCheckListLivraison, 
      vehicle_id :vehicleSelected!.vehicle_id, 
      onSuccess: (response){
        loading(false);
        success.call(response.message);
        
      },
      onFailure: (response){
        if (response.statusCode == Strings.common.expiredTokenCode){
          UserRemoteSA().logout();
          loading(false);
          failure?.call(response);
        }
        else {
          loading(false);
          failure?.call(response);
        }

      }
    );
  }
}