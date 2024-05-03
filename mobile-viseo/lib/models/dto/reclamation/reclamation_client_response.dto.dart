import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/devis/owner_devis.dto.dart';
import 'package:sav/models/dto/reclamation/owner_reclamation.dto.dart';

class ReclamationClientResponseDto extends BaseResponseDto {
  late OwnerReclamationDto data;
  ReclamationClientResponseDto():super();

  ReclamationClientResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = OwnerReclamationDto.fromJson(jsonData);
    }
  }
}