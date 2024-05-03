import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/contact/contact_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class ContactRemoteRepo{
  BaseRemoteBDL get _helper => BaseRemoteBDL();

  Future<ContactResponseDto> getContact() async {
    var response = await _helper.get(
      "${Urls.contact.contactList}",
    );
    return ContactResponseDto.fromJson(response);
  }
}