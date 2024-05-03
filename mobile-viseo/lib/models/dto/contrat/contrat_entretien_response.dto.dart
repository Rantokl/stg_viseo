import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/contrat/contrat_entretien.dto.dart';

class ContratEntretienResponseDto extends BaseResponseDto {
  late List<ContratEntretienDto> data = [];
  ContratEntretienResponseDto():super();

  ContratEntretienResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
        .map((item) => ContratEntretienDto.fromJson(item))
        .toList();
    }
  }
}