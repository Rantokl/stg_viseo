import 'package:camera/camera.dart';

import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/upload/upload_vehicle.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/remote/upload/upload_vehicle_remote.sa.dart';

class ViewImgController extends BaseController {
  ViewImgController(
    this.img
  ) : super();
  final XFile img; 
  
  late UploadVehicleRemoteSA service;

  @override
  void onInit() {
    super.onInit();
    this.service = UploadVehicleRemoteSA();
  }
  
  
  uploadVehicle({
    required CompletionClosure<bool> success,
    CompletionClosure<BaseResponseDto>? failure
  }) async {
    loading(true);
    UploadVehicleDto vehicleDto = UploadVehicleDto(image: img.path);
    await service.uploadVehicle(
        vehicleId: vehicleSelected!.vehicle_id,
        vehicle: vehicleDto,
        onSuccess: (response) {
          loading(false);
          success.call(true);
        },
        onFailure: (response) {
          failure?.call(response);
        }
    );
  }
}