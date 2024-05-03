import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/camera/view_img.controller.dart';
import 'package:sav/presentations/controllers/vehicle/vehicle_list.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';

class ViewImgView extends BaseStatelessView<ViewImgController> {
  ViewImgView({
    Key? key,
    required this.img,
  }) : super(key: key, controller: Get.put(ViewImgController(img))) {}

  final XFile img; 

  late double _screenWidth;
  late double _screenHeight;

  void uploadVehicle() async {
    await controller.uploadVehicle(
      success: (success) {
        if(success) {
          Get.find<VehiculeController>().getUserCar(
            success: (success) {
              
              Get.back();
            }
          );
        }
      },
      failure: (res) {
        Get.back();
      }
    );
  }

  @override
  Widget build(BuildContext context) {
    _screenWidth = MediaQuery.of(context).size.width;
  _screenHeight = MediaQuery.of(context).size.height;
    return baseScaffoldView(
        appBarController: AppBarController(
            title: "Photo"
        ),
        withHeader: true,
        body:  Padding(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          mainAxisSize: MainAxisSize.min, 
          children: [
            VerticalSpace.m,
            if (img != null) ...[
              Image.file(File(img!.path), fit: BoxFit.cover, width: _screenWidth, height: _screenHeight * 55 / 100,),
            ],
            VerticalSpace.m,
            CustomeButton.elevated(
              fontSize: ThemeSpacing.m,
              buttonTitle: "Envoyer",
              onPressed: uploadVehicle, 
              color: ThemeColors.green
            )
          ]),
      ),
      );
  }
}
