import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/devis/devis_validation.dto.dart';

class DevisValidationResponseDto extends BaseResponseDto {
  late DevisValidationdto data;

  DevisValidationResponseDto():super();

  DevisValidationResponseDto.fromJson(dynamic json) : super.fromJson(json) {
    var jsonData = getData(json);
    if ((json != null) && (jsonData != null)) {
      this.data = DevisValidationdto.fromJson(jsonData);
    }
  }
}