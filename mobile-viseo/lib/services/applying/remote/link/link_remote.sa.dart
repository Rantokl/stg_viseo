import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/link/link_reponse.dto.dart';
import 'package:sav/repository/remote/link/link_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';


class LinkRemoteSA extends BaseRemoteSA {

  final repository = LinkRemoteRepo();

  getLink ({
    required CompletionClosure<LinkResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
     var response = await repository.getLink();
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