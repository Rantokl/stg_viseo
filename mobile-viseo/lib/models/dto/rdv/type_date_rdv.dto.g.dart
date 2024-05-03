// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'type_date_rdv.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

TypeDateRdvDto _$TypeDateRdvDtoFromJson(Map<String, dynamic> json) =>
    TypeDateRdvDto(
      type_rendez_vous_id: json['type_rendez_vous_id'] as int,
      date_rendez_vous: json['date_rendez_vous'] as String,
    );

Map<String, dynamic> _$TypeDateRdvDtoToJson(TypeDateRdvDto instance) =>
    <String, dynamic>{
      'type_rendez_vous_id': instance.type_rendez_vous_id,
      'date_rendez_vous': instance.date_rendez_vous,
    };
