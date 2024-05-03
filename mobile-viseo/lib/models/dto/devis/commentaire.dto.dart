import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'commentaire.dto.g.dart';

@JsonSerializable()
class CommentaireDto extends BaseDto {
  int commentaire_id;
  int devis_id;
  int owner_id;
  
  CommentaireDto({required this.commentaire_id, required this.devis_id, required this.owner_id});

  factory CommentaireDto.fromJson(dynamic json) {
    return _$CommentaireDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.commentaire_id = serializable.commentaire_id;
    this.owner_id = serializable.owner_id;
    this.devis_id = serializable.devis_id;
  }

  @override
  CommentaireDto copy() => CommentaireDto(commentaire_id: this.commentaire_id, devis_id: this.devis_id, owner_id: this.owner_id)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$CommentaireDtoToJson(this);
}