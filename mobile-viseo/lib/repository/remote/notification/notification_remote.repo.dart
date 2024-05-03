import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/notification/notification_reponse.dto.dart';
import 'package:sav/models/dto/notification/push_notification_response.dto.dart';
import 'package:sav/models/dto/notification/push_notification.dto.dart';
import 'package:sav/models/dto/notification/read_notification.dto.dart';
import 'package:sav/models/dto/notification/read_notification_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class NotificationRemoteRepo {
  BaseRemoteBDL get helper => BaseRemoteBDL();

  Future<PushNotificationResponseDto> postToken(PushNotificationDto request) async {
    var response = await helper.post(
        "${Urls.notification.fbm}/",
        body: request.toJsonLocal()
    );
    return PushNotificationResponseDto.fromJson(response);
  }

  Future<NotificationResponseDto> getNotif() async {
    var response = await helper.get(
      "${Urls.notification.notif}/",
    ); 
    return NotificationResponseDto.fromJson(response);
  }

  Future<ReadNotificationResponseDto> readNotif(int notifId) async {
    var response = await helper.put(
      "${Urls.notification.read}/$notifId/",
      ""
    ); 
    return ReadNotificationResponseDto.fromJson(response);
  }

}