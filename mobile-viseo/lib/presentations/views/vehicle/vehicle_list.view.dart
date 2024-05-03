import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_svg/svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/presentations/controllers/vehicle/vehicle_list.controller.dart';
import 'package:sav/presentations/views/auth/login.view.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';
import 'package:sav/presentations/views/widgets/input/custom_input.widget.dart';

import '../widgets/modal/modal.widget.dart';


class VehiculeView extends BaseStatelessView<VehiculeController>{
  VehiculeView({Key? key}): super(key: key,controller: Get.put(VehiculeController())) {
    WidgetsBinding.instance!.addPostFrameCallback((_) {
        if (!controller.isLoaded.value) {
                controller.getUserCar(
                    success: (success) {

                    },
                    failure: (response) {
                      if (response.statusCode == Strings.common.expiredTokenCode) {
                        showTokenExpiredModal();
                      }
                    }
                );
                controller.isLoaded.value = true;
              }
    });

    controller.searchbarcrtl.addListener(() {
       text.value = controller.searchbarcrtl.text;
       controller.getSearchCar(controller.searchbarcrtl.text);
    });
  }

RxString text = "".obs;

@override
Widget build(BuildContext context) {
  double textScale = MediaQuery.of(context).textScaleFactor;
  return Column(
    mainAxisAlignment: MainAxisAlignment.start,
    children: [
      Padding(
        padding: EdgeInsets.symmetric(vertical: 10),
        child: CustomInput(
          line: 1,
          label: "Numéro du véhicule",
          suffixIcon: Icon(Icons.search, color: ThemeColors.dark,),
          controller: controller.searchbarcrtl,
        ),
      ),
      Obx(() => controller.isLoading
          ? Container()
          : controller.isTokenExpired.value ? Container() :  text.value.length == 0
              ? _buildGridView(controller.userCar.value!.data, textScale)
              : controller.searchCar.value?.data?.isNotEmpty == true
                  ? _buildGridView(controller.searchCar.value!.data, textScale)
                  : Center(
                      child: Text(
                        'Aucun véhicule correspondant',
                        style: TextStyle(color: ThemeColors.white),
                      ),
                    )
          ),
    ],
  );
}

Widget _buildGridView(List<VehicleDto> vehicles, double textScale) {
  return Expanded(
    child: GridView.builder(
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisSpacing: 10,
          mainAxisSpacing: 10,
          crossAxisCount: 2,
          childAspectRatio: 0.7 / textScale),
      itemCount: vehicles.length,
      itemBuilder: (context, index) {
        var vehicule = vehicles[index];
        return CustomCard.Vehicle(
                  vehiculeDto: vehicule,
                  textScale: textScale,
                  onTap: () {
                    controller.vehicleSelected = vehicule;
                    pushNamed(
                      routeName: Routes.vehicleDetail,
                    );
                  },
                  onTapPic: () {
                    controller.vehicleSelected = vehicule;
                    pushNamed(
                      routeName: Routes.camera,
                    );
                  }
              );
      },
    ),
  );
}
}