import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/upload/owner_vehicle_image.dto.dart';
import 'package:sav/models/dto/user/profile.dto.dart';

class UploadVehicleResponseDto extends BaseResponseDto {
  late OwnerVehicleImgDto data;

  UploadVehicleResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = OwnerVehicleImgDto.fromJson(jsonData);
    }
  }
}