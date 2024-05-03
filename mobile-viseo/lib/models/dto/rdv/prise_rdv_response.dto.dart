import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/menu/owner.dto.dart';

class PriseRdvResponseDto extends BaseResponseDto {
  late OwnerDto data;
  PriseRdvResponseDto():super();

  PriseRdvResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = OwnerDto.fromJson(jsonData);
    }
  }
}
