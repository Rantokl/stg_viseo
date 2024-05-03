import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/rdv/heure_prise_rdv.dto.dart';

class HeurePriseRdvResponseDto extends BaseResponseDto {
  List<HeurePriseRdvDto> data = [];
  HeurePriseRdvResponseDto():super();

  HeurePriseRdvResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = getData(json);
    if ((json != null) && (jsonData != null)) {

      var data_tmp = (jsonData as List<dynamic>)
          .map((item) => HeurePriseRdvDto.fromJson(item))
          .toList();

      this.data = data_tmp.map((e) => HeurePriseRdvDto(date_rendez_vous: e.date_rendez_vous, heure_rendez_vous: e.heure_rendez_vous.substring(0,5))).toList();
    }

  }
}
