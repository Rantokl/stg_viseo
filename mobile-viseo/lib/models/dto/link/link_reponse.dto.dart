import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/link/link.dto.dart';

class LinkResponseDto extends BaseResponseDto {
  late LinkDto data;

  LinkResponseDto():super();

  LinkResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = LinkDto.fromJson(jsonData);
    }
  }
}