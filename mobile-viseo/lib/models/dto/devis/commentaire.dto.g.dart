// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'commentaire.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

CommentaireDto _$CommentaireDtoFromJson(Map<String, dynamic> json) =>
    CommentaireDto(
      commentaire_id: json['commentaire_id'] as int,
      devis_id: json['devis_id'] as int,
      owner_id: json['owner_id'] as int,
    );

Map<String, dynamic> _$CommentaireDtoToJson(CommentaireDto instance) =>
    <String, dynamic>{
      'commentaire_id': instance.commentaire_id,
      'devis_id': instance.devis_id,
      'owner_id': instance.owner_id,
    };
