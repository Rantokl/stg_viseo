import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/chat/room.dto.dart';

class RoomResponseDto extends BaseResponseDto {
  late RoomDto data;

  RoomResponseDto():super();

  RoomResponseDto.fromJson(dynamic json) : super.fromJson(json) {
    var jsonData = getData(json);
    if ((json != null) && (jsonData != null)) {
      this.data = RoomDto.fromJson(jsonData);
    }
  }
}