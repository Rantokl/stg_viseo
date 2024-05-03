import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/panic/send_panic.dto.dart';

class SendPanicResponseDto extends BaseResponseDto {
  late SendPanicDto data;

  SendPanicResponseDto():super();

  SendPanicResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = SendPanicDto.fromJson(jsonData);
    }
  }
}