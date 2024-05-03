import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/contact/contact_response.dto.dart';
import 'package:sav/repository/remote/contact/contact_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';

class ContactRemoteSA extends BaseRemoteSA{
  final contactRepository = ContactRemoteRepo();

  getContact({
    required CompletionClosure<ContactResponseDto> onSuccess,
    CompletionClosure<BaseResponseDto>? onFailure
  }) async {
    var response = await contactRepository.getContact();
    switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response);
        break;
    }
  }
}