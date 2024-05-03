import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/rdv/date_actuelle_response.dto.dart';
import 'package:sav/models/dto/rdv/heure_prise_rdv_response.dto.dart';
import 'package:sav/models/dto/rdv/mes_rdv_response.dto.dart';
import 'package:sav/models/dto/rdv/prise_rdv.dto.dart';
import 'package:sav/models/dto/rdv/prise_rdv_response.dto.dart';
import 'package:sav/models/dto/rdv/type_date_rdv.dto.dart';
import 'package:sav/models/dto/rdv/type_rdv_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class RdvRemoteRepo{
  BaseRemoteBDL get _helper => BaseRemoteBDL();

  // Prise rdv
  Future<PriseRdvResponseDto> postPriseRdv(PriseRdvDto priseRdvDto, int vehicleId) async {
    var response = await _helper.post(
      "${Urls.rdv.priseRdv}/$vehicleId/",
      body: priseRdvDto.toJsonLocal(),
    );
    return PriseRdvResponseDto.fromJson(response);
  }

  Future<PriseRdvResponseDto> updateRdv(PriseRdvDto priseRdvDto, int vehicleId, int rdvId) async {
    var response = await _helper.post(
      "${Urls.rdv.updateRdv}/$vehicleId/$rdvId/",
      body: priseRdvDto.toJsonLocal(),
    );
    return PriseRdvResponseDto.fromJson(response);
  }

  Future<TypeRdvResponseDto> getTypeRdv() async {
    var response = await _helper.get(
      "${Urls.rdv.typeRdv}",
    );
    return TypeRdvResponseDto.fromJson(response);
  }

  // Mes rdv
  Future<MesRdvResponseDto> getMesRdv() async {
    var response = await _helper.get(
      "${Urls.rdv.mesRdv}",
    );
    return MesRdvResponseDto.fromJson(response);
  }

  Future<HeurePriseRdvResponseDto> getHeurePriseRdv(TypeDateRdvDto typeDateRdvDto) async {
    var response = await _helper.get(
      "${Urls.rdv.heurePrise}/${typeDateRdvDto.date_rendez_vous}",
    );
    return HeurePriseRdvResponseDto.fromJson(response);
  }

   Future<DateActuelleResponseDto> getDateActuelle() async {
    var response = await _helper.get(
      "${Urls.rdv.dateActuelle}/",
    );
    return DateActuelleResponseDto.fromJson(response);
  }
}