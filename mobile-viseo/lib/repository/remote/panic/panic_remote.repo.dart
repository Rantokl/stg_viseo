import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/devis/type_devis_response.dto.dart';
import 'package:sav/models/dto/panic/panic_response.dto.dart';
import 'package:sav/models/dto/panic/send_panic_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class PanicRemoteRepo {
  BaseRemoteBDL get helper => BaseRemoteBDL();

  Future<PanicResponseDto> getMenuPanic() async {
    var response = await helper.get(
      "${Urls.panic.menuPanic}/",
    );    
    return PanicResponseDto.fromJson(response);
  }

  Future<SendPanicResponseDto> postPanic(int panic_id) async {
    var response = await helper.post(
        "${Urls.panic.sendPanic}/${panic_id.toString()}/",
    );
    return SendPanicResponseDto.fromJson(response);
  }

}