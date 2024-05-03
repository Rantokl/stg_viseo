// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'evaluation.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

EvaluationDto _$EvaluationDtoFromJson(Map<String, dynamic> json) =>
    EvaluationDto(
      evaluation: (json['evaluation'] as List<dynamic>)
          .map(QuestionResultDto.fromJson)
          .toList(),
      commentaire: json['commentaire'] as String?,
    );

Map<String, dynamic> _$EvaluationDtoToJson(EvaluationDto instance) =>
    <String, dynamic>{
      'evaluation': EvaluationDto.toPrestation(instance.evaluation),
      'commentaire': instance.commentaire,
    };
