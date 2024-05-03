import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/rdv/date_actuelle.dto.dart';

class DateActuelleResponseDto extends BaseResponseDto {
  late DateActuelleDto data;

  DateActuelleResponseDto():super();

  DateActuelleResponseDto.fromJson(Map<String, dynamic> json)
    :super.fromJson(json) {
      var jsonData = json['data'];
      print(jsonData);
      data = DateActuelleDto.fromJson(jsonData);
    }
}