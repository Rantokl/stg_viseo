import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'question.dto.g.dart';

@JsonSerializable()
class QuestionDto extends BaseDto {
  int id;
  String question_evaluation;
  
  QuestionDto({required this.id, required this.question_evaluation});

  factory QuestionDto.fromJson(dynamic json) {
    return _$QuestionDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.id = serializable.id;
    this.question_evaluation = serializable.question_evaluation;
  }

  @override
  QuestionDto copy() => QuestionDto(id: this.id, question_evaluation: this.question_evaluation)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$QuestionDtoToJson(this);

}