import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/evaluation/question_result.dto.dart';

part 'list_question_result.dto.g.dart';

@JsonSerializable()
class ListQuestionResultDto extends BaseDto {
  @JsonKey(toJson: toPrestation)
  List<QuestionResultDto> questions;
  String? commentaire;
  
  ListQuestionResultDto({required this.questions, required this.commentaire});

  factory ListQuestionResultDto.fromJson(dynamic json) {
    return _$ListQuestionResultDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.questions = serializable.questions;
    this.commentaire = serializable.commentaire;
  }

  @override
  ListQuestionResultDto copy() => ListQuestionResultDto(questions: this.questions, commentaire: this.commentaire)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$ListQuestionResultDtoToJson(this);

  static List<Map<String, dynamic>> toPrestation(List<QuestionResultDto> values){
      return values.map((e) => e.toJsonLocal()).toList();
  }

}