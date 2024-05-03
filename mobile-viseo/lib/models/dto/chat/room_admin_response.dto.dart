import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/chat/room.dto.dart';

class RoomAdminResponseDto extends BaseResponseDto {
  List<RoomDto> data = [];
  RoomAdminResponseDto():super();

  RoomAdminResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = getData(json);
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
          .map((item) => RoomDto.fromJson(item))
          .toList();
    }
  }
}
