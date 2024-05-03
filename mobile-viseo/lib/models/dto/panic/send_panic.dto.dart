import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'send_panic.dto.g.dart';

@JsonSerializable()
class SendPanicDto extends BaseDto {
  String to;
  int owner_id;
  
  SendPanicDto({required this.to, required this.owner_id});

  factory SendPanicDto.fromJson(dynamic json) {
    return _$SendPanicDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.to = serializable.to;
    this.owner_id = serializable.owner_id;
  }

  @override
  SendPanicDto copy() => SendPanicDto(to: this.to, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$SendPanicDtoToJson(this);

}