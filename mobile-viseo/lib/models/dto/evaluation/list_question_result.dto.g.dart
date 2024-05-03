// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'list_question_result.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ListQuestionResultDto _$ListQuestionResultDtoFromJson(
        Map<String, dynamic> json) =>
    ListQuestionResultDto(
      questions: (json['questions'] as List<dynamic>)
          .map(QuestionResultDto.fromJson)
          .toList(),
      commentaire: json['commentaire'] as String?,
    );

Map<String, dynamic> _$ListQuestionResultDtoToJson(
        ListQuestionResultDto instance) =>
    <String, dynamic>{
      'questions': ListQuestionResultDto.toPrestation(instance.questions),
      'commentaire': instance.commentaire,
    };
