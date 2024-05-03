import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/rdv/mes_rdv.dto.dart';

class MesRdvResponseDto extends BaseResponseDto {
  List<MesRdvDto> data = [];
  MesRdvResponseDto():super();

  MesRdvResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = getData(json);
    if ((json != null) && (jsonData != null)) {

    var data_tmp = (jsonData as List<dynamic>)
        .map((item) => MesRdvDto.fromJson(item))
        .toList();

    this.data = data_tmp.map((e) => MesRdvDto(id_rdv: e.id_rdv, number_vehicle: e.number_vehicle, type_rdv: e.type_rdv, date_rdv: e.date_rdv, heure_rdv: e.heure_rdv.substring(0,5), message: e.message, vehicle: e.vehicle, status_rdv: e.status_rdv)).toList();
    }

  }
}
