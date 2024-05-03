// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'contact.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ContactDto _$ContactDtoFromJson(Map<String, dynamic> json) => ContactDto(
      nom: json['nom'] as String?,
      telephone: json['téléphone'] as String?,
      siege: json['siège'] as String?,
      type_contact_id: json['type_contact_id'] as String,
    );

Map<String, dynamic> _$ContactDtoToJson(ContactDto instance) =>
    <String, dynamic>{
      'nom': instance.nom,
      'téléphone': instance.telephone,
      'siège': instance.siege,
      'type_contact_id': instance.type_contact_id,
    };
