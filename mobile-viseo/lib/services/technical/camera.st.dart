import 'package:camera/camera.dart';

class CameraST {
  Future<CameraController?> InitCamera(CameraController cameraController) async {
    if (!cameraController.value.isInitialized) {
      try {
        await cameraController.initialize().then((_) async {
          if (cameraController.value.isInitialized) {
            cameraController.startImageStream((image) => null);
          }
          return cameraController;
        });
      } on CameraException catch (e) {
        print("camera error $e");
      }
    }

    return cameraController;
  }
}
