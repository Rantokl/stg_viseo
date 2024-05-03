import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/mdpOublier/mdp_oublier.dto.dart';
import 'package:sav/models/dto/user/user.dto.dart';

class MdpOublierResponseDto extends BaseResponseDto {
  late MdpOublierDto data;

  MdpOublierResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = MdpOublierDto.fromJson(jsonData);
    }
  }
}