import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/notification/notification_reponse.dto.dart';
import 'package:sav/models/dto/notification/push_notification_response.dto.dart';
import 'package:sav/models/dto/notification/push_notification.dto.dart';
import 'package:sav/models/dto/notification/read_notification_response.dto.dart';
import 'package:sav/repository/remote/notification/notification_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';


class NotificationRemoteSA extends BaseRemoteSA {

  final repository = NotificationRemoteRepo();


  postfbm ({
    required PushNotificationDto request,
    required CompletionClosure<PushNotificationResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await repository.postToken(request);
     switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

  getNotif ({
    required CompletionClosure<NotificationResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
     var response = await repository.getNotif();
     switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }


  readNotif ({
    required int notifId,
    required CompletionClosure<ReadNotificationResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await repository.readNotif(notifId);
     switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }
   
}