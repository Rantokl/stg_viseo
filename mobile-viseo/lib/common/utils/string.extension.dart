import 'package:flutter/material.dart';
import 'package:strings/strings.dart';

extension Parsing on String {
  int toInt() {
    try {
      return int.parse(this.toNumberFormat());
    } on Exception {
      return 0;
    }
  }

  double toDouble() {
    if (this.isEmpty)
      return 0;
    else
      return double.parse(this.toNumberFormat());
  }

  DateTime? toDateTime() {
    if (this == null) {
      return null;
    }
    return DateTime.parse(this);
  }

  String? toStringDateTime() {
    if (this == null) {
      return null;
    }

    var splitted = this.split("/");

    if (splitted.length == 3) {
      return "${splitted[2]}-${splitted[1]}-${splitted[0]}";
    } else
      return this;
  }

  Color toHexToColor() {
    return new Color(int.parse(this.substring(1, 7), radix: 16) + 0xFF000000);
  }

  TimeOfDay? toTimeOfDay() {
    if (this == null) {
      return null;
    }

    var splitted = this.split(":");
    return (splitted.length == 2)
        ? TimeOfDay(hour: splitted.first.toInt(), minute: splitted.last.toInt())
        : null;
  }

  String? toStringDateFormat() {
    if (this == null) {
      return null;
    }

    var splitted = this.replaceAll("-", "/").split("/");

    if (splitted.length == 3) {
      return "${splitted[2]}-${splitted[1]}-${splitted[0]}";
    } else
      return this;
  }


  DateTime? toDateFormat() {
    if (this == null) {
      return null;
    }

    var dateString = this.toStringDateFormat();

    if (dateString != null)
      return dateString.toDateTime();
    else
      return null;
  }
}

extension Methods on String {
  String dropSpace() => this.replaceAll(" ", "").trim();

  bool isNotNull() => (this != null);

  bool isNullOrEmpty({bool trim = false}) {
    if (this == null) {
      return true;
    }
    return (trim) ? this.trim().isEmpty : this.isEmpty;
  }

  int lastIndex() {
    if ((this == null) || (this.isEmpty)) {
      return -1;
    }
    return this.length - 1;
  }

  String? firstOrNull() {
    if ((this == null) || (this.isEmpty)) {
      return null;
    }
    return this[0];
  }

  String? lastOrNull() {
    if ((this == null) || (this.isEmpty)) {
      return null;
    }
    return this[this.lastIndex()];
  }

  String? extension() {
    if ((this == null) || (this.isEmpty)) {
      return null;
    }
    return ".${this.split(".").last}";
  }

  bool isNumeric() {
    if (this == null) {
      return false;
    }
    return double.tryParse(this) != null;
  }
}

extension StringFormat on String {

  String toNumberFormat() => this.dropSpace().replaceAll(",", ".");

  String capitalizeFirstLettersOnly() {
    String result = "";
    var splitted = this.split(" ");
    splitted.forEach((word) {
      if (word.length == 1) {
        result += word.toUpperCase();
      } else if (word.length > 1) {
        result += "${word.firstOrNull()?.toUpperCase()}"
            "${word.substring(1).toLowerCase()} ";
      }
    });
    return result.trim();
  }

}