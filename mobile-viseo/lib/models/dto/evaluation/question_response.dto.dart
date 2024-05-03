import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/evaluation/question.dto.dart';

class QuestionResponseDto extends BaseResponseDto {
  late List<QuestionDto> data = [];

  QuestionResponseDto():super();

  QuestionResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['questions'];
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
        .map((item) => QuestionDto.fromJson(item))
        .toList();
    }
  }
}