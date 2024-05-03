import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/reclamation/type_reclamation.dto.dart';

class TypeReclamationResponseDto extends BaseResponseDto {
  late List<TypeReclamationDto> data;

  TypeReclamationResponseDto():super();

  TypeReclamationResponseDto.fromJson(Map<String, dynamic> json)
      : super.fromJson(json) {
    var jsonData = json['reclamations'];
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
          .map((item) => TypeReclamationDto.fromJson(item))
          .toList();
    }
  }
}