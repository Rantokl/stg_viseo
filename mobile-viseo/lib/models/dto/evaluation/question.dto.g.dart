// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'question.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

QuestionDto _$QuestionDtoFromJson(Map<String, dynamic> json) => QuestionDto(
      id: json['id'] as int,
      question_evaluation: json['question_evaluation'] as String,
    );

Map<String, dynamic> _$QuestionDtoToJson(QuestionDto instance) =>
    <String, dynamic>{
      'id': instance.id,
      'question_evaluation': instance.question_evaluation,
    };
