import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/chat/owner_chat.dto.dart';

class ChatSendResponseDto extends BaseResponseDto {
  late OwnerChatDto data;
  ChatSendResponseDto():super();

  ChatSendResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = OwnerChatDto.fromJson(jsonData);
    }
  }
}