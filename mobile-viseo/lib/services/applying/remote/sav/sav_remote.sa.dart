import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/sav/sav_response.dto.dart';
import 'package:sav/repository/remote/sav/sav_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';


class SavRemoteSA extends BaseRemoteSA {

  final repository = SavRemoteRepo();

  getSav ({
    required int vehicle_id,
    required CompletionClosure<SavResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
     var response = await repository.getSav(vehicle_id);
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