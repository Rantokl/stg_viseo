import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/garantie/carnet_garantie.dto.dart';

class CarnetGarantieResponseDto extends BaseResponseDto {
  late List<CarnetGarantieDto> data = [];
  CarnetGarantieResponseDto():super();

  CarnetGarantieResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
        .map((item) => CarnetGarantieDto.fromJson(item))
        .toList();
    }
  }
}