import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/mdpOublier/email.dto.dart';
import 'package:sav/models/dto/mdpOublier/mdp_oublier_reponse.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class MdpOublierRemoteRepo {
  BaseRemoteBDL get helper => BaseRemoteBDL();

  Future<MdpOublierResponseDto> postEmail(EmailDto email) async {
    var response = await helper.post(
      "${Urls.mdpOublier.mdpOublier}/",
      body: email.toJsonLocal(),
      tokenRequired: false,
    ); 
    return MdpOublierResponseDto.fromJson(response);
  }

}