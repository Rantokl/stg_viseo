import 'package:sav/models/base_synchonizable.dart';

const String tempString = "string";
const int tempInt = 0;
const double tempReal = 0.0;

abstract class BaseDo extends BaseSynchronizable {
  int? get currentLocalId => localId;

  BaseDo();

  BaseDo.fromJson(dynamic json) : super.fromJson(json);

  BaseDo initTempFields();

  BaseDo fromJson(dynamic json);

  Map<String, dynamic> removeLocalFields(Map<String, dynamic> json) {
    json.remove(localIdKey);
    json.remove(localStateKey);
    return json;
  }
}