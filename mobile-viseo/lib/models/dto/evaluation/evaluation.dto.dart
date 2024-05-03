import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/evaluation/question_result.dto.dart';

part 'evaluation.dto.g.dart';

@JsonSerializable()
class EvaluationDto extends BaseDto {
  @JsonKey(toJson: toPrestation)
  List<QuestionResultDto> evaluation;
  String? commentaire;
  
  EvaluationDto({required this.evaluation, required this.commentaire});

  factory EvaluationDto.fromJson(dynamic json) {
    return _$EvaluationDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.evaluation = serializable.evaluation;
    this.commentaire = serializable.commentaire;
  }

  @override
  EvaluationDto copy() => EvaluationDto(evaluation: this.evaluation, commentaire: this.commentaire)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$EvaluationDtoToJson(this);

  static List<Map<String, dynamic>> toPrestation(List<QuestionResultDto> values){
      return values.map((e) => e.toJsonLocal()).toList();
  }

}
