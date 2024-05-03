import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/devis/type_devis.dto.dart';

class TypeDevisResponseDto extends BaseResponseDto {
  late List<TypeDevisDto> data = [];

  TypeDevisResponseDto():super();

  TypeDevisResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['type_devis'];
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
        .map((item) => TypeDevisDto.fromJson(item))
        .toList();
    }
  }
}