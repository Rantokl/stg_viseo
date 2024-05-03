import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';

part 'devis_commentaire.dto.g.dart';

@JsonSerializable()
class DevisCommentaire extends BaseDto {
  String commentaire;
  
  DevisCommentaire({required this.commentaire});

  factory DevisCommentaire.fromJson(dynamic json) {
    return _$DevisCommentaireFromJson(json);
  }

  @override
  bind(serializable) {
    this.commentaire = serializable.commentaire;
  }

  @override
  DevisCommentaire copy() => DevisCommentaire(commentaire: this.commentaire)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$DevisCommentaireToJson(this);

  @override
  String toString() {
    // TODO: implement toString
    return commentaire;
  }
}