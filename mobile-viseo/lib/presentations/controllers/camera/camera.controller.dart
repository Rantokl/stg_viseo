import 'package:camera/camera.dart';

import 'package:get/get.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/technical/camera.st.dart';

class CamController extends BaseController {
  
  late CameraController cameraController;
  CameraST camera = CameraST();
  var indexCam = 0.obs;
  var nbCamera = 0.obs;
  RxBool cameraInitialize = false.obs;
  RxList<CameraDescription> ListCamera = RxList<CameraDescription>([]);

  @override
  onInit() {
    super.onInit();
    camera = CameraST();
    firstInitCamera();
  }

  @override
  void onReady() {
    super.onReady();
  }

  firstInitCamera() async {
    List<CameraDescription> ListCameras = await availableCameras();
    ListCamera.value = ListCameras;
    initCamera();
  }

  initCamera() async {
    cameraController = CameraController(
      ListCamera[indexCam.value], 
      ResolutionPreset.high, 
      enableAudio: false,
      imageFormatGroup: ImageFormatGroup.yuv420,
      );
    try{
      var camController = await camera.InitCamera(cameraController);
      if(camController != null) {
        cameraController = camController;
        cameraInitialize.value = cameraController.value.isInitialized;
      }
    } catch (e) {
      print(" ========== $e");
    }
  }

   switchCam() async {
    print(indexCam);
    if(indexCam.value + 1 < ListCamera.length) {
      indexCam.value += 1;
    } else {
      indexCam.value -= 1;
    }
    await cameraController.dispose();  
    initCamera();
  }


}