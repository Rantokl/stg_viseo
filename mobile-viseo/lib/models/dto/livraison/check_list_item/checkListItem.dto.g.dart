// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'checkListItem.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

CheckListItemDto _$CheckListItemDtoFromJson(Map<String, dynamic> json) =>
    CheckListItemDto(
      items_id: json['items_id'] as int,
      details_id: json['details_id'] as int,
      status: json['status'] as bool,
    );

Map<String, dynamic> _$CheckListItemDtoToJson(CheckListItemDto instance) =>
    <String, dynamic>{
      'items_id': instance.items_id,
      'details_id': instance.details_id,
      'status': instance.status,
    };
