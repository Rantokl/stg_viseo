// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'list_checkListLivraison.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ListCheckListLivraison _$ListCheckListLivraisonFromJson(
        Map<String, dynamic> json) =>
    ListCheckListLivraison(
      items: (json['items'] as List<dynamic>)
          .map(CheckListItemDto.fromJson)
          .toList(),
      commentaire: json['commentaire'] as String,
      stateId: json['state_id'] as int,
    );

Map<String, dynamic> _$ListCheckListLivraisonToJson(
        ListCheckListLivraison instance) =>
    <String, dynamic>{
      'items': ListCheckListLivraison.toCheckListLivraison(instance.items),
      'commentaire': instance.commentaire,
      'state_id': instance.stateId,
    };
