import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get/get_connect/http/src/utils/utils.dart';
import 'package:image_picker/image_picker.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/presentations/controllers/camera/camera.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';

class CameraView extends BaseStatelessView<CamController> {
  CameraView({
    Key? key,
  }) : super(key: key, controller: Get.put(CamController())) {}

  Future takePicture() async {
    if (!controller.cameraController.value.isInitialized) {
      return null;
    }
    if (controller.cameraController.value.isTakingPicture) {
      return null;
    }
    try {
      await controller.cameraController.setFlashMode(FlashMode.off);
      XFile picture = await controller.cameraController.takePicture();
      pushNamed(routeName: Routes.image, arguments: {"img": picture}, addToBack: false);
    } on CameraException catch (e) {
      print('Error occured while taking picture: $e');
      return null;
    }
  }

  Future selectImageFromGallery() async {
  final ImagePicker _picker = ImagePicker();
  final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if(image != null) {
      pushNamed(routeName: Routes.image, arguments: {"img": image}, addToBack: false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: SafeArea(
      child: Stack(
        children: [
          Obx(
            () => (controller.cameraInitialize.value)
                ? Container(
                  height: double.infinity,
                  child: CameraPreview(
                      controller.cameraController,
                    ),
                )
                : Container(
                    color: Colors.black,
                    child: const Center(child: CircularProgressIndicator())),
          ),
          Align(
                          alignment: Alignment.bottomCenter,
                          child: Container(
                              height: MediaQuery.of(context).size.height * 0.20,
                              decoration: const BoxDecoration(
                                  borderRadius:
                                      BorderRadius.vertical(top: Radius.circular(24)),
                                  color: Colors.black),
                              child: Row(
                                  crossAxisAlignment: CrossAxisAlignment.center,
                                  children: [
                                    Expanded(
                                      child: Container(), // Ajouté cette ligne pour occuper l'espace à gauche
                                    ),
                                    Expanded(
                                      child: IconButton(
                                      onPressed: takePicture,
                                      iconSize: 50,
                                      padding: EdgeInsets.zero,
                                      constraints: const BoxConstraints(),
                                      icon: Icon(Icons.circle, color: Colors.white),
                                      ),
                                    ),
                                    Expanded(
                                      child: IconButton(
                                      padding: EdgeInsets.zero,
                                      iconSize: 30,
                                      icon: Icon( Icons.image_outlined ,color: Colors.white),
                                      onPressed: selectImageFromGallery,
                                    )),
                                  ]),
                            ),
                        ),
        ],
      ),
    ));
  }
}
