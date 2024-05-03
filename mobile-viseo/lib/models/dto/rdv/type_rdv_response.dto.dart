import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/rdv/type_rdv.dto.dart';

class TypeRdvResponseDto extends BaseResponseDto {
  late List<TypeRdvDto> data;

  TypeRdvResponseDto():super();

  TypeRdvResponseDto.fromJson(Map<String, dynamic> json)
      : super.fromJson(json) {
    var jsonData = getData(json);
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
          .map((item) => TypeRdvDto.fromJson(item))
          .toList();
    }
  }
}