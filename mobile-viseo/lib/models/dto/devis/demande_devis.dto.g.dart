// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'demande_devis.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

demandeDevisDto _$demandeDevisDtoFromJson(Map<String, dynamic> json) =>
    demandeDevisDto(
      type_devis_id: json['type_devis_id'] as int,
      details: json['details'] as String,
      pdf: json['pdf'] as String?,
      prix: json['prix'] as String?,
      resume: json['resume'] as String?,
      numero_devis: json['numero_devis'] as String?,
    );

Map<String, dynamic> _$demandeDevisDtoToJson(demandeDevisDto instance) =>
    <String, dynamic>{
      'type_devis_id': instance.type_devis_id,
      'details': instance.details,
      'pdf': instance.pdf,
      'prix': instance.prix,
      'resume': instance.resume,
      'numero_devis': instance.numero_devis,
    };
