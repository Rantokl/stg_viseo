import 'package:sav/models/base.serializable.dart';
import 'package:sav/models/base_synchonizable.dart';

abstract class BaseDto extends BaseSerializable {
}

abstract class BaseSynchronizableDto extends BaseSynchronizable {
  Map<String, dynamic> toJsonRequest();

  Map<String, dynamic> localFieldsRemoved(Map<String, dynamic> json) {
    var result = json;
    result?.remove(localIdKey);
    result?.remove(localStateKey);
    return result;
  }
}