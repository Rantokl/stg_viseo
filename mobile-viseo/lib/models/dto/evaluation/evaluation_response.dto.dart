import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/evaluation/evaluation.dto.dart';

class EvaluationResponseDto extends BaseResponseDto {
  late EvaluationDto data;

  EvaluationResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = EvaluationDto.fromJson(jsonData);
    }
  }
}