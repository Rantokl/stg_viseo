import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'question_result.dto.g.dart';

@JsonSerializable()
class QuestionResultDto extends BaseDto {
  int question_id;
  int note_id;
  
  QuestionResultDto({required this.question_id, required this.note_id});

  factory QuestionResultDto.fromJson(dynamic json) {
    return _$QuestionResultDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.question_id = serializable.question_id;
    this.note_id = serializable.note_id;
  }

  @override
  QuestionResultDto copy() => QuestionResultDto(question_id: this.question_id, note_id: this.note_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$QuestionResultDtoToJson(this);

}