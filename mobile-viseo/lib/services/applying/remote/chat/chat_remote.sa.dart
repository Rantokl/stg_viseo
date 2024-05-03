import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/chat/chat_send.dto.dart';
import 'package:sav/models/dto/chat/chat_send_response.dto.dart';
import 'package:sav/models/dto/chat/room_admin_response.dto.dart';
import 'package:sav/models/dto/chat/room_response.dto.dart';
import 'package:sav/repository/remote/chat/chat_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

class ChatRemoteSA extends BaseRemoteSA{
  final chatRepo = ChatRemoteRepo();

  postConversation ({
    required int roomId,
    required ChatSendDto request,
    required CompletionClosure<ChatSendResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await chatRepo.postConversation(roomId, request);
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

  getConversation ({
    required int roomId,
    required CompletionClosure<RoomResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await chatRepo.getConversation(roomId);
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

  getAdminConversation ({
    required CompletionClosure<RoomAdminResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await chatRepo.getAdminConversation();
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