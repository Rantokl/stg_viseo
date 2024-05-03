abstract class BaseSerializable {

  Map<String, dynamic> toJsonLocal();

  dynamic copy();

  bind(dynamic serializable);

}