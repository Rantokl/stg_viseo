

import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/devis/devis.dto.dart';

class ListDevisResponseDto extends BaseResponseDto {
  List<DevisDto> data = [];
  ListDevisResponseDto() : super();

  ListDevisResponseDto.fromJson(Map<String, dynamic> json)
        : super.fromJson(json) {
        var jsonData = getData(json);
        if ((json != null) && (jsonData != null)) {
            this.data = (jsonData as List<dynamic>)
                .map((item) => DevisDto.fromJson(item))
                .toList();
        }
    }
}