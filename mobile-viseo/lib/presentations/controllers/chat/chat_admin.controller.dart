import 'dart:math';

import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/chat/room.dto.dart';
import 'package:sav/models/dto/chat/room_admin_response.dto.dart';
import 'package:sav/models/dto/user/profile_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/chat/chat_remote.sa.dart';
import 'package:intl/intl.dart';
import 'package:sav/services/applying/remote/user_remonte.sa.dart';

class ChatAdminController extends BaseController {
  ChatAdminController() : super();
  PreferenceSA pref = PreferenceSA.instance;
  late ChatRemoteSA service;
  late UserRemoteSA userService;
  late Rx<RoomAdminResponseDto?> inboxMessage = Rx<RoomAdminResponseDto?>(null);
  late Rx<ProfileResponseDto?> profileResponse = Rx<ProfileResponseDto?>(null);
  List<Map<String, dynamic>> discussions = [];

  @override
  onInit() {
    super.onInit();
    this.service = ChatRemoteSA();
    this.userService = UserRemoteSA();
  }

  @override
  void onReady() async {
    super.onReady();
    await getConversationList();
  }

  Future<void> getConversationList() async {
    loading(true);

    await service.getAdminConversation(
        onSuccess: (response) async {
          inboxMessage.value = response;

          for (var msg in inboxMessage.value!.data) {
            await userService.getProfile(userId: msg.client_id, onSuccess: (response) {
              profileResponse.value = response;
              var dateMessage = DateTime.parse(msg.messages.last.time).add(Duration(hours: 3));
              String formattedDate = "${dateMessage.day.toString().padLeft(2, '0')} ${getMonthName(dateMessage.month - 1)} à ${dateMessage.hour.toString().padLeft(2, '0')}:${dateMessage.minute.toString().padLeft(2, '0')}";
              discussions.add({
                "lastMessage": msg.messages.last.message_text,
                "time" : formattedDate,
                "username": profileResponse.value!.data.username,
                "roomId": msg.room_id
              });
            });

          }
          loading(false);
        },
        onFailure: (message) {
          print(message);
        }
    );

  }

  logout({
    required CompletionClosure<bool> success,
    CompletionClosure<String>? failure
  }) async {
    loading(true);
    await userService.logout(
      onSuccess: (res) {
          loading(false);
          success.call(true);
        },
        onFailure: (message) {
          loading(false);
          failure?.call(message);
        }
    );
  }


  String getMonthName(int number){
    var monthNames = [
      'janvier',
      'février',
      'mars',
      'avril',
      'mai',
      'juin',
      'juillet',
      'août',
      'septembre',
      'octobre',
      'novembre',
      'décembre',
    ];
    return monthNames[number];
  }

}

