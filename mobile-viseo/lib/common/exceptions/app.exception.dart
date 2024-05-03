class AppException implements Exception {
  String _message = "";
  String _prefix = "";

  AppException(this._message , this._prefix);

  set message(String message) {
    this._message = message;
  }

  String get message => this._message;

  set prefix(String prefix) {
    this._prefix = prefix;
  }

  String get prefix => this._prefix;

  String toString() {
    return "$_prefix $_message";
  }
}