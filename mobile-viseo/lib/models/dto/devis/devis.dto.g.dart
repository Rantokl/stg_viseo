// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'devis.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

DevisDto _$DevisDtoFromJson(Map<String, dynamic> json) => DevisDto(
      devis_id: json['devis_id'] as int,
      type_devis: json['type_devis'] as String,
      numero_devis: json['numero_devis'] as String?,
      prix: json['prix'] as String?,
      resume: json['resume'] as String?,
      details: json['details'] as String,
      date_upload_devis: json['date_upload_devis'] as String?,
      date_devis: json['date_devis'] as String,
      status_devis: json['status_devis'] as String,
      pdf: json['pdf'] as String?,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$DevisDtoToJson(DevisDto instance) => <String, dynamic>{
      'devis_id': instance.devis_id,
      'type_devis': instance.type_devis,
      'numero_devis': instance.numero_devis,
      'prix': instance.prix,
      'resume': instance.resume,
      'details': instance.details,
      'date_devis': instance.date_devis,
      'date_upload_devis': instance.date_upload_devis,
      'status_devis': instance.status_devis,
      'pdf': instance.pdf,
      'owner_id': instance.owner_id,
    };
