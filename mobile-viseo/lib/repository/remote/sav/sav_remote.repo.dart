import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/sav/sav_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class SavRemoteRepo {
  BaseRemoteBDL get helper => BaseRemoteBDL();

  Future<SavResponseDto> getSav(int vehicle_id) async {
    var response = await helper.get(
      "${Urls.sav.sav}/$vehicle_id",
    );    
    return SavResponseDto.fromJson(response);
  }

}