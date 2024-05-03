import 'package:json_annotation/json_annotation.dart';

import 'package:sav/models/dto/base.dto.dart';

part 'checkListItem.dto.g.dart';

@JsonSerializable()
class CheckListItemDto extends BaseDto {
  int items_id;
  int details_id;
  bool status;

  CheckListItemDto({
    required this.items_id,
    required this.details_id,
    required this.status,
  });

  factory CheckListItemDto.fromJson(dynamic json){
    return _$CheckListItemDtoFromJson(json);
  }
  
  @override
  bind(serializable) {
    this.items_id = serializable.items_id;
    this.details_id = serializable.details_id;
    this.status = serializable.status;
  }
  
  @override
  CheckListItemDto copy() => CheckListItemDto(items_id: this.items_id, details_id : this.details_id, status: this.status);
  
  @override
  Map<String, dynamic> toJsonLocal() => _$CheckListItemDtoToJson(this);
}
