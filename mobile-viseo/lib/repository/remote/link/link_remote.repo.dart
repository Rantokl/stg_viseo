import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/link/link_reponse.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class LinkRemoteRepo {
  BaseRemoteBDL get helper => BaseRemoteBDL();

  Future<LinkResponseDto> getLink() async {
    var response = await helper.get(
      "${Urls.link.link}/",
    ); 
    return LinkResponseDto.fromJson(response);
  }

}