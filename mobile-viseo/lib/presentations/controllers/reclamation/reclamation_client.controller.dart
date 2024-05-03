import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/reclamation/reclamation_client.dto.dart';
import 'package:sav/models/dto/reclamation/type_reclamation.dto.dart';
import 'package:sav/models/dto/reclamation/type_reclamation_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/reclamation/reclamation_remote.sa.dart';

import '../../../services/applying/remote/user_remonte.sa.dart';

class ReclamationClientController extends BaseController {
  ReclamationClientController() : super();
  PreferenceSA pref = PreferenceSA.instance;
  late ReclamationRemoteSA service;
  late Rx<TypeReclamationResponseDto?> typeReclamation = Rx<TypeReclamationResponseDto?>(null);
  TextEditingController messageReclamationCtrl = TextEditingController();

  TypeReclamationDto selectedTypeReclamation = TypeReclamationDto(id: 0, libelle: "");
  ReclamationClientDto reclamationClientDto = ReclamationClientDto(type_reclamation_id: 0, message: "");
  var messageResponse = "";

  List textDescription = [
    {
      "text": Strings.reclamation.reclamationIndication,
      "size": 15.0,
      "isBold": true,
    },
    {
      "text": Strings.reclamation.reclamationRequired,
    }
  ];

  @override
  void onInit() {
    super.onInit();
    this.service = ReclamationRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
    getTypeReclamation();
  }

  String? dropdownTypeReclamationValidator(TypeReclamationDto? value){
    if (value == null) {
      return Strings.common.fieldRequired;
    }

    return null;
  }

  getTypeReclamation() async {
    loading(true);
    await service.getTypeReclamation(
        onSuccess: (response) {
          typeReclamation.value = response;
          selectedTypeReclamation = typeReclamation.value!.data.first;
          loading(false);
        },
        onFailure: (error) {
          print(error);
          loading(false);
        }
    );
  }

  postReclamationClient({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
  }
      ) async {
    loading(true);
    reclamationClientDto.type_reclamation_id = selectedTypeReclamation.id;
    reclamationClientDto.message = messageReclamationCtrl.text;
    await service.postReclamationClient(vehicleId: pref.vehicle!.vehicle_id, reclamationClientDto: reclamationClientDto,
        onSuccess: (res){
          print(res.message);
          messageResponse = res.message;
          loading(false);
          success?.call(true);
        },
        onFailure: (response){
          if (response.statusCode == Strings.common.expiredTokenCode){
            UserRemoteSA().logout();
            loading(false);
            failure?.call(response);
          }else{
            print(response);
            messageResponse = response.message;
            loading(false);
            failure?.call(response);
          }
        }
    );
  }

}