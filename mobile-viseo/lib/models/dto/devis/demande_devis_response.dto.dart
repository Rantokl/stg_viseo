import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/devis/owner_devis.dto.dart';
import 'package:sav/models/dto/menu/owner.dto.dart';

class DemandeDevisResponseDto extends BaseResponseDto {
  late OwnerDevisDto data;
  DemandeDevisResponseDto():super();

  DemandeDevisResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = OwnerDevisDto.fromJson(jsonData);
    }
  }
}