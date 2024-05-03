import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/models/dto/devis/commentaire.dto.dart';

class DevisCommentaireResponseDto extends BaseResponseDto {
  late CommentaireDto data;
  DevisCommentaireResponseDto():super();

  DevisCommentaireResponseDto.fromJson(Map<String, dynamic> json) : super.fromJson(json) {
    var jsonData = json['data'];
    if ((json != null) && (jsonData != null)) {
      this.data = CommentaireDto.fromJson(jsonData);
    }
  }
}