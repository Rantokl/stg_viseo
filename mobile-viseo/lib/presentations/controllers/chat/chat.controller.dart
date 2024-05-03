import 'dart:math';

import 'package:get/get.dart';
import 'package:mime/mime.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/chat/chat_send.dto.dart';
import 'package:sav/models/dto/chat/room_response.dto.dart';
import 'package:sav/models/dto/user/profile_response.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:http/http.dart' as http;
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:sav/services/applying/remote/chat/chat_remote.sa.dart';
import 'package:sav/services/applying/remote/user_remonte.sa.dart';

class ChatController extends BaseController {
  ChatController({required this.roomId, required this.username}) : super();
  PreferenceSA pref = PreferenceSA.instance;
  late ChatRemoteSA service;
  late UserRemoteSA userService;
  final int roomId; // utilisé seulement si Admin est connecté
  final String username;
  ChatSendDto req = ChatSendDto(sender: 0, message_text: "");
  String message_send = "";
  late Rx<RoomResponseDto?> inboxRoomMessage = Rx<RoomResponseDto?>(null);
  TextEditingController messageController = TextEditingController();
  RxList<types.Message> messages = RxList<types.Message>([]);
  var user;
  var otherUser;

  @override
  onInit() async {
    super.onInit();
    user = types.User(id: prefs.user!.id.toString() + randomString());
    otherUser = types.User(id: roomId.toString() + randomString(), firstName: username);
    this.service = ChatRemoteSA();
    this.userService = UserRemoteSA();
  }

  @override
  void onReady() async {
    super.onReady();
    await getConversation();
  }

  postConversation({
    required CompletionClosure<bool> success,
    CompletionClosure<String>? failure
  }) async {
    req.sender = prefs.user!.id;
    req.message_text = message_send;
    loading(true);
    await service.postConversation(
        roomId: roomId,
        request: req,
        onSuccess: (res) {
          loading(false);
          success.call(true);
        },
        onFailure: (message) {
          print(message);
          loading(false);
          failure?.call(message);
        }
    );
  }

  Future<void> getConversation() async {
    loading(true);

    await service.getConversation(
        roomId: (prefs.profile!.isAdmin) ? roomId : prefs.user!.room_id!,
        onSuccess: (response) {
          inboxRoomMessage.value = response;
          for (var msg in inboxRoomMessage.value!.data.messages) {
            final myMessage = types.TextMessage(
              author: (msg.sender == prefs.user!.id) ? user : otherUser,
              createdAt: DateTime
                  .parse(msg.time)
                  .millisecondsSinceEpoch,
              id: randomString(),
              text: msg.message_text,
              status: types.Status.seen,
            );
            _addMessage(myMessage);
          }
          loading(false);
        },
        onFailure: (message) {
          print(message);
          loading(false);
        }
    );
  }

  String randomString() {
    final random = Random.secure();
    final values = List<int>.generate(16, (i) => random.nextInt(255));
    return base64UrlEncode(values);
  }

  _addMessage(types.Message message) {
    messages.insert(0, message);
  }

  handleMessageTap(BuildContext _, types.Message message) async {
    loading(true);
    if (message is types.FileMessage) {
      var localPath = message.uri;

      if (message.uri.startsWith('http')) {
        try {
          final index =
          messages.indexWhere((element) => element.id == message.id);
          final updatedMessage =
          (messages[index] as types.FileMessage).copyWith(
            isLoading: true,
          );

          messages[index] = updatedMessage;
        } finally {
          final index =
          messages.indexWhere((element) => element.id == message.id);
          final updatedMessage =
          (messages[index] as types.FileMessage).copyWith(
            isLoading: null,
          );

          messages[index] = updatedMessage;
        }
      }
      loading(false);
    }
    loading(false);
  }

  handlePreviewDataFetched(types.TextMessage message,
      types.PreviewData previewData,) {
    loading(true);
    final index = messages.indexWhere((element) => element.id == message.id);
    final updatedMessage = (messages[index] as types.TextMessage).copyWith(
      previewData: previewData,
    );

    messages[index] = updatedMessage;
    loading(false);
  }

  handleSendPressed(types.PartialText message) {
    loading(true);
    final textMessage = types.TextMessage(
      author: user,
      createdAt: DateTime
          .now()
          .millisecondsSinceEpoch,
      id: randomString(),
      text: message.text,
    );

    _addMessage(textMessage);

    message_send = message.text;

    postConversation(
        success: (isSucces) {
          if (isSucces) {
            print("Message envoyé");
          }
        },
        failure: (message) {
          print("Erreur lors de l'envoi du message");
        }
    );

    loading(false);
  }

  Future<void> handleEndReached() async {
    // messages.clear();
    // await getConversation();
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
}

