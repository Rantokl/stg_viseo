import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/chat/chat_send.dto.dart';
import 'package:sav/models/dto/chat/chat_send_response.dto.dart';
import 'package:sav/models/dto/chat/room_admin_response.dto.dart';
import 'package:sav/models/dto/chat/room_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class ChatRemoteRepo {
  BaseRemoteBDL get helper => BaseRemoteBDL();

  Future<RoomResponseDto> getConversation(int roomId) async {
    var response = await helper.get(
      "${Urls.chat.checkRoom}/$roomId/",
    );
    return RoomResponseDto.fromJson(response);
  }

  Future<RoomAdminResponseDto> getAdminConversation() async {
    var response = await helper.get(
      "${Urls.chat.checkRoomAdmin}/",
    );
    return RoomAdminResponseDto.fromJson(response);
  }

  Future<ChatSendResponseDto> postConversation(int roomId, ChatSendDto request) async {
    var response = await helper.post(
        "${Urls.chat.updateRoomMessage}/$roomId/",
        body: request.toJsonLocal()
    );

    return ChatSendResponseDto.fromJson(response);
  }


}