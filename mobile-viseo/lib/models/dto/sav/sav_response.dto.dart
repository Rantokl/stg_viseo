import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/sav/sav.dto.dart';

class SavResponseDto extends BaseResponseDto {
  late List<SavDto> data;

  SavResponseDto():super();

  SavResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
        .map((item) => SavDto.fromJson(item))
        .toList();
    }
  }
}