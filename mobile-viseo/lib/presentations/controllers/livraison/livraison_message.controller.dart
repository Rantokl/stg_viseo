
import 'package:flutter/cupertino.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/livraison/check_list_item/checkListItem.dto.dart';
import 'package:sav/models/dto/livraison/check_list_item/list_checkListLivraison.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/presentations/controllers/livraison/livraison_check.controller.dart';
import 'package:sav/services/applying/remote/livraison/livraison_remote.sa.dart';

import '../../../services/applying/remote/user_remonte.sa.dart';

class LivraisonMessageController extends BaseController{
  LivraisonMessageController() : super();
  late LivraisonRemoteSA service;
  TextEditingController messageReclamationCtrl = TextEditingController();
   List textDescription = [
    {
      "text": Strings.livraison.indication,
      "size": 15.0,
      "isBold": true,
    },
    {
      "text": Strings.livraison.required,
    }
  ];

   @override
  onInit() {
    super.onInit();
    this.service = LivraisonRemoteSA();
  }

    @override
  void onReady() {
    super.onReady();
  }

  postCheckListItemsWithMessage({
    required  List<CheckListItemDto> listCheckListItemDto,
    required CompletionClosure<String> success,
    CompletionClosure<BaseResponseDto>? failure,

  }) async {
    ListCheckListLivraison listCheckListLivraison = ListCheckListLivraison(items: listCheckListItemDto, commentaire: messageReclamationCtrl.text, stateId: 3);
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