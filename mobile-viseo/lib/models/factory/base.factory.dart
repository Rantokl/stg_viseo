import 'package:sav/models/base.data.dart';
import 'package:sav/models/domain_object/base.do.dart';

class BaseFactory<Do extends BaseDo, Dto> {
  Do? toDomainObject(Dto dto) => null;

  Dto? toDataTransfertObject(BaseDo domainObject) => null;

  List<Do?> toDomainObjects(List<Dto> list) => list.map((dto) {
    return toDomainObject(dto);
  }).toList();

  List<Dto?> toDataTransfertObjects(List<BaseDo> list) =>
      list.map((domainObject) {
        return toDataTransfertObject(domainObject);
      }).toList();

  int boolToInt(bool value) => BaseData.boolToInt(value);

  bool intToBool(int value) => BaseData.intToBool(value);

  String? intListToString(List<int> values) => BaseData.intListToString(values);

  List<int>? stringToIntList(String value) => BaseData.stringToIntList(value);

  String? stringListToString(List<String> values) => BaseData.stringListToString(values);

  List<String>? stringToStringList(String value) => BaseData.stringToStringList(value);
}