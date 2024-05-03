
import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'check_list_livraison_detail.dto.g.dart';

@JsonSerializable()
class CheckListLivraisonDetailDto extends BaseDto{
  String? categorie;
  int id;
  String libelle;
  bool isChecked;

  CheckListLivraisonDetailDto({
    required this.categorie,
    required this.id,
    required this.libelle,
    required this.isChecked
  });

  factory CheckListLivraisonDetailDto.fromJson(dynamic json) {
    if(json['isChecked'] == null) json['isChecked'] = false;
    return _$CheckListLivraisonDetailDtoFromJson(json);
  }
  
  @override
  bind(serializable) {
    this.categorie = serializable.categorie;
    this.id = serializable.id;
    this.libelle = serializable.libelle;
  }
  
  @override
  CheckListLivraisonDetailDto copy() => CheckListLivraisonDetailDto(categorie: this.categorie, id: this.id, libelle: this.libelle, isChecked: this.isChecked)..bind(this);
  
  @override
  Map<String, dynamic> toJsonLocal() => _$CheckListLivraisonDetailDtoToJson(this);
}