// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'check_list_livraison_detail.dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

CheckListLivraisonDetailDto _$CheckListLivraisonDetailDtoFromJson(
        Map<String, dynamic> json) =>
    CheckListLivraisonDetailDto(
      categorie: json['categorie'] as String?,
      id: json['id'] as int,
      libelle: json['libelle'] as String,
      isChecked: json['isChecked'] as bool,
    );

Map<String, dynamic> _$CheckListLivraisonDetailDtoToJson(
        CheckListLivraisonDetailDto instance) =>
    <String, dynamic>{
      'categorie': instance.categorie,
      'id': instance.id,
      'libelle': instance.libelle,
      'isChecked': instance.isChecked,
    };
