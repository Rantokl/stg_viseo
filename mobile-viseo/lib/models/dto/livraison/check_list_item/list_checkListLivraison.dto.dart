// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/base.dto.dart';
import 'package:sav/models/dto/livraison/check_list_item/checkListItem.dto.dart';

part 'list_checkListLivraison.dto.g.dart';

@JsonSerializable()
class ListCheckListLivraison extends BaseDto {
  @JsonKey(toJson: toCheckListLivraison)
  List<CheckListItemDto> items;
  String commentaire;
  @JsonKey(name: 'state_id')
  int stateId;
  ListCheckListLivraison({
    required this.items,
    required this.commentaire,
    required this.stateId,
  });
  @override
  bind(serializable) {
     this.items = serializable.items;
  }

  @override
  copy() => ListCheckListLivraison(items: this.items, commentaire: this.commentaire, stateId: this.stateId);

  @override
  Map<String, dynamic> toJsonLocal() => _$ListCheckListLivraisonToJson(this);

  static List<Map<String, dynamic>> toCheckListLivraison(List<CheckListItemDto> values){
    return values.map((e) => e.toJsonLocal()).toList();
  }

}
