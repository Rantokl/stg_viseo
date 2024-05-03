import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/panic/panic.dto.dart';

class PanicResponseDto extends BaseResponseDto {
  late List<PanicDto> data;

  PanicResponseDto():super();

  PanicResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['menus_panique'];
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
        .map((item) => PanicDto.fromJson(item))
        .toList();
    }
  }
}