import 'package:get/get.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/livraison/check_list_livraison/check_list_livraison.dto.dart';

class CheckListLivraisonResponseDto extends BaseResponseDto {
  List<CheckListLivraisonDto> data = [];
  late int checkListstatus = 0;

  CheckListLivraisonResponseDto():super();

  CheckListLivraisonResponseDto.fromJsonByVehicle(Map<String, dynamic> json)
      : super.fromJson(json) {
        print(json);
        if(json != null && json["data"] != null && !json["data"].isEmpty) {
          print('RESPNSE ETO');
          this.data = (json["data"]["data_checklist"] as List<dynamic>)
              .map((item) {
                CheckListLivraisonDto test = CheckListLivraisonDto.fromJson(item);
                return test;
              })
              .toList();
          this.checkListstatus = json["data"]["status"];
        }
        // if(json["data"]["status"] != null){
        //   this.checkListstatus = json["data"]["status"];
        // }
      }
  CheckListLivraisonResponseDto.fromJson(Map<String, dynamic> json)
      : super.fromJson(json) {
        print(json);
        if(json != null && json["data"] != null && !json["data"].isEmpty) {
          print('RESPNSE ETO');
          this.data = (json["data"] as List<dynamic>)
              .map((item) {
                CheckListLivraisonDto test = CheckListLivraisonDto.fromJson(item);
                return test;
              })
              .toList();
          this.checkListstatus = 0;
        }
      }

}