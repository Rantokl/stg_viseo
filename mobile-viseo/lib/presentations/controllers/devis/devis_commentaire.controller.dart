import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/devis/devis_commentaire.dto.dart';
import 'package:sav/models/dto/devis/devis_commentaire_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/devis/devis_remote.sa.dart';

import '../../../models/constant/values/strings.dart';
import '../../../services/applying/remote/user_remonte.sa.dart';

class DevisCommentaireController extends BaseController {
  
  final TextEditingController commentaireCrtl = TextEditingController();
  late DevisRemoteSA service;
  PreferenceSA pref = PreferenceSA.instance;
  Rx<DevisCommentaireResponseDto?> typeDevis = Rx<DevisCommentaireResponseDto?>(null);
  var messageResponse = "";
  DevisCommentaire req = DevisCommentaire(commentaire: "");
  
  @override
  onInit() {
    super.onInit();
    this.service = DevisRemoteSA();
  }

  postDevisCommentaire({
    required int id,
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
  }) async {
    req.commentaire = commentaireCrtl.text;
    loading(true);
    await service.devisCommentaire(
      id: id,
      request: req, 
      onSuccess: (res) {
          print(res.message);
          messageResponse = res.message;
          loading(false);
          success.call(true);
        },
        onFailure: (response) {
          if (response.statusCode == Strings.common.expiredTokenCode){
            UserRemoteSA().logout();
            loading(false);
            failure?.call(response);
          }else{
            print(response.message);
            messageResponse = response.message;
            loading(false);
            failure?.call(response);
          }
        }
    );
  }
}