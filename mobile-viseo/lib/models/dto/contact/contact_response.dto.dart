import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/contact/contact.dto.dart';


class ContactResponseDto extends BaseResponseDto {
  late List<ContactDto> data;

  ContactResponseDto():super();

  ContactResponseDto.fromJson(Map<String, dynamic> json)
      : super.fromJson(json) {
    var jsonData = json["contacts"];
    if ((json != null) && (jsonData != null)) {
      this.data = (jsonData as List<dynamic>)
          .map((item) => ContactDto.fromJson(item))
          .toList();
    }
  }
}