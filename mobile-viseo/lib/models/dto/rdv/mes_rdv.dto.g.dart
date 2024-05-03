// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'mes_rdv.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

MesRdvDto _$MesRdvDtoFromJson(Map<String, dynamic> json) => MesRdvDto(
      id_rdv: json['id_rdv'] as int,
      vehicle:
          (json['vehicle'] as List<dynamic>).map(VehicleDto.fromJson).toList(),
      type_rdv: json['type_rdv'] as String,
      date_rdv: json['date_rdv'] as String,
      heure_rdv: json['heure_rdv'] as String,
      number_vehicle: json['number_vehicle'] as String,
      message: json['message'] as String,
      status_rdv: json['status_rdv'] as String,
    );

Map<String, dynamic> _$MesRdvDtoToJson(MesRdvDto instance) => <String, dynamic>{
      'id_rdv': instance.id_rdv,
      'vehicle': instance.vehicle,
      'type_rdv': instance.type_rdv,
      'date_rdv': instance.date_rdv,
      'heure_rdv': instance.heure_rdv,
      'number_vehicle': instance.number_vehicle,
      'status_rdv': instance.status_rdv,
      'message': instance.message,
    };
