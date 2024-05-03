// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'heure_prise_rdv.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

HeurePriseRdvDto _$HeurePriseRdvDtoFromJson(Map<String, dynamic> json) =>
    HeurePriseRdvDto(
      date_rendez_vous: json['date_rendez_vous'] as String,
      heure_rendez_vous: json['heure_rendez_vous'] as String,
    );

Map<String, dynamic> _$HeurePriseRdvDtoToJson(HeurePriseRdvDto instance) =>
    <String, dynamic>{
      'date_rendez_vous': instance.date_rendez_vous,
      'heure_rendez_vous': instance.heure_rendez_vous,
    };
