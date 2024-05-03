import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/livraison/check_list_livraison/check_list_livraison_detail.dto.dart';

part 'check_list_livraison.dto.g.dart';

@JsonSerializable()
class CheckListLivraisonDto extends BaseDto {
  int items_id;
  String label;
  List<CheckListLivraisonDetailDto> details;

  CheckListLivraisonDto({
    required this.items_id,
    required this.label,
    required this.details
  });

  factory CheckListLivraisonDto.fromJson(dynamic json) {
    return _$CheckListLivraisonDtoFromJson(json);
  }
  
  @override
  bind(serializable) {
    this.items_id = serializable.items_id;
    this.label = serializable.label;
    this.details = serializable.details;
  }
  
  @override
  CheckListLivraisonDto copy() => CheckListLivraisonDto(items_id: this.items_id, label: this.label, details: this.details);
  
  @override
  Map<String, dynamic> toJsonLocal() => _$CheckListLivraisonDtoToJson(this);
}