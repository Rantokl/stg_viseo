// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'check_list_livraison.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

CheckListLivraisonDto _$CheckListLivraisonDtoFromJson(
        Map<String, dynamic> json) =>
    CheckListLivraisonDto(
      items_id: json['items_id'] as int,
      label: json['label'] as String,
      details: (json['details'] as List<dynamic>)
          .map(CheckListLivraisonDetailDto.fromJson)
          .toList(),
    );

Map<String, dynamic> _$CheckListLivraisonDtoToJson(
        CheckListLivraisonDto instance) =>
    <String, dynamic>{
      'items_id': instance.items_id,
      'label': instance.label,
      'details': instance.details,
    };
