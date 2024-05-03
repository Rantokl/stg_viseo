
import 'dart:convert';

import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/livraison/check_list_item/list_checkListLivraison.dto.dart';
import 'package:sav/models/dto/livraison/check_list_livraison/check_list_livraison_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';
import 'package:sav/models/dto/base_response.dto.dart';

class LivraisonRemoteRepo{
  BaseRemoteBDL get _helper => BaseRemoteBDL();

  Future<CheckListLivraisonResponseDto> getOptionListLivraisonByVehicle(int idVehicle) async {
    var response = await _helper.get(
      "${Urls.livraison.checkListLivraisonByVehicle}/${idVehicle}"
    );
    return CheckListLivraisonResponseDto.fromJsonByVehicle(response);
  }
  Future<CheckListLivraisonResponseDto> getOptionListLivraison() async {
    var response = await _helper.get(
      "${Urls.livraison.checkListLivraison}"
    );
    return CheckListLivraisonResponseDto.fromJson(response);
  }

  Future<BaseResponseDto> postCheckListItems(ListCheckListLivraison listCheckListLivraison, int vehicle_id) async {
    var response = await _helper.post(
      "${Urls.livraison.checklistItems}/${vehicle_id}/",
      body: listCheckListLivraison.toJsonLocal()
    );
    return BaseResponseDto.fromJson(response);
  }
}