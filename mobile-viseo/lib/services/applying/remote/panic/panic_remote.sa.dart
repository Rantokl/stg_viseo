import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/panic/panic_response.dto.dart';
import 'package:sav/models/dto/panic/send_panic_response.dto.dart';
import 'package:sav/repository/remote/panic/panic_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';


class PanicRemoteSA extends BaseRemoteSA {

  final repository = PanicRemoteRepo();

  getMenuPanic ({
    required CompletionClosure<PanicResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
     var response = await repository.getMenuPanic();
     switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

  postPanic ({
    required int panic_id,
    required CompletionClosure<SendPanicResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await repository.postPanic(panic_id);
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