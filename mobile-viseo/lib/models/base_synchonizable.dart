
import 'package:sav/models/base.serializable.dart';

const localIdKey = "localId";
const localStateKey = "localState";

class BaseSynchronizable extends BaseSerializable {
  int? localId;
  int? localState;

  BaseSynchronizable({this.localId});

  BaseSynchronizable.fromJson(dynamic json) {
    if (json != null) {
      this.localId = json[localIdKey];
      this.localState = json[localStateKey];
    }
  }

  @override
  bind(serializable) {
    this.localId = serializable?.localId;
    this.localState = serializable?.localState;
  }

  @override
  BaseSynchronizable copy() =>
      BaseSynchronizable()
        ..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() =>
      <String, dynamic>{
        localIdKey: this.localId,
        localStateKey: this.localState
      };
}

class LocalState {
  static const none = 0;
  static const synchronized = 1;
  static const created = 2;
  static const updated = 3;
}