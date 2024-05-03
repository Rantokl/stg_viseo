// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'question_result.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

QuestionResultDto _$QuestionResultDtoFromJson(Map<String, dynamic> json) =>
    QuestionResultDto(
      question_id: json['question_id'] as int,
      note_id: json['note_id'] as int,
    );

Map<String, dynamic> _$QuestionResultDtoToJson(QuestionResultDto instance) =>
    <String, dynamic>{
      'question_id': instance.question_id,
      'note_id': instance.note_id,
    };
