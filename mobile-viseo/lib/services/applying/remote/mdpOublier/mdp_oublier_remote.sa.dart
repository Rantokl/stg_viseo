import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/link/link_reponse.dto.dart';
import 'package:sav/models/dto/mdpOublier/email.dto.dart';
import 'package:sav/models/dto/mdpOublier/mdp_oublier_reponse.dto.dart';
import 'package:sav/repository/remote/link/link_remote.repo.dart';
import 'package:sav/repository/remote/mdpOublier/mdp_oublier_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';


class MdpOublierRemoteSA extends BaseRemoteSA {

  final repository = MdpOublierRemoteRepo();

  postEmail ({
    required EmailDto email,
    required CompletionClosure<MdpOublierResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
     var response = await repository.postEmail(email);
     switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }   
}