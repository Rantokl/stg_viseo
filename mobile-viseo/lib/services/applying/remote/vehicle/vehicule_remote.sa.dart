import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/vehicle/search_vehicule_response.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle_response.dto.dart';
import 'package:sav/repository/remote/vehicle/vehicule_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

import '../user_remonte.sa.dart';

class VehiculeRemoteSA extends BaseRemoteSA {

  final repository = VehiculeRemoteRepo();

  getUserCar ({
    required int id,
    required CompletionClosure<VehiculeResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {

    var response = await repository.getUserCar(id);
    switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response);

        break;
    }
  }

  Future<bool> checkToken({required int id,
    }) async
  {
    var checkValue = false;
    var responseCheckToken = await repository.getUserCar(id);
    switch (responseCheckToken.succes) {
      case true:
        return true;
      default:
        await UserRemoteSA().refreshToken(
          onSuccess: (success) {
            checkValue = success;
          },
          onFailure: (failure) {

            checkValue = failure;
          }
        );
    }
    return checkValue;
  }

  getSearchCar ({
    required String number,
    required CompletionClosure<VehiculeResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await repository.getSearchCar(number);
     switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

}