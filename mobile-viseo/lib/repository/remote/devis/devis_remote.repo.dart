import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/devis/demande_devis.dto.dart';
import 'package:sav/models/dto/devis/demande_devis_response.dto.dart';
import 'package:sav/models/dto/devis/type_devis_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';
import 'package:sav/models/dto/devis/devis_commentaire.dto.dart';
import 'package:sav/models/dto/devis/devis_commentaire_response.dto.dart';
import 'package:sav/models/dto/devis/devis_validation_response.dto.dart';
import 'package:sav/models/dto/devis/list_devis_response.dto.dart';

class DevisRemoteRepo {
  BaseRemoteBDL get helper => BaseRemoteBDL();

  Future<TypeDevisResponseDto> getTypeDevis() async {
    var response = await helper.get(
      "${Urls.devis.typeDevis}/",
    );    
    return TypeDevisResponseDto.fromJson(response);
  }

  Future<DemandeDevisResponseDto> postDemandeDevis(demandeDevisDto request, int vehicle_id) async {
    var response = await helper.post(
        "${Urls.devis.demandeDevis}/${vehicle_id.toString()}/",
        body: request.toJsonLocal(),
    );
    return DemandeDevisResponseDto.fromJson(response);
  }

  Future<ListDevisResponseDto> getListDevis (int id) async {
    var response = await helper.get(
      "${Urls.devis.listDevis}/$id/" ,
    );
    return ListDevisResponseDto.fromJson(response);
  }

  Future<DevisValidationResponseDto> validationDevis (int id, int validation) async {
    var response = await helper.post(
      "${Urls.devis.validationDevis}/$id/$validation/"
    );
    return DevisValidationResponseDto.fromJson(response);
  }

  Future<DevisCommentaireResponseDto> devisCommentaire (int id,  DevisCommentaire request) async {
    var response = await helper.post(
      "${Urls.devis.postCommentaire}/$id/",
      body: request.toJsonLocal()
    );
    return DevisCommentaireResponseDto.fromJson(response);
  }
}