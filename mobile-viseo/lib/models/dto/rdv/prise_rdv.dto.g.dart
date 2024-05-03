// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'prise_rdv.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

PriseRdvDto _$PriseRdvDtoFromJson(Map<String, dynamic> json) => PriseRdvDto(
      type_rendez_vous_id: json['type_rendez_vous_id'] as int,
      date_rendez_vous: json['date_rendez_vous'] as String,
      heure_rendez_vous: json['heure_rendez_vous'] as String,
      message: json['message'] as String,
    );

Map<String, dynamic> _$PriseRdvDtoToJson(PriseRdvDto instance) =>
    <String, dynamic>{
      'type_rendez_vous_id': instance.type_rendez_vous_id,
      'date_rendez_vous': instance.date_rendez_vous,
      'heure_rendez_vous': instance.heure_rendez_vous,
      'message': instance.message,
    };
