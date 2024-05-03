// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'devis_validation.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

DevisValidationdto _$DevisValidationdtoFromJson(Map<String, dynamic> json) =>
    DevisValidationdto(
      devis_id: json['devis_id'] as int,
      owner_id: json['owner_id'] as int,
      status_devis: json['status_devis'] as String,
      pdf: json['pdf'] as String,
    );

Map<String, dynamic> _$DevisValidationdtoToJson(DevisValidationdto instance) =>
    <String, dynamic>{
      'devis_id': instance.devis_id,
      'pdf': instance.pdf,
      'status_devis': instance.status_devis,
      'owner_id': instance.owner_id,
    };
