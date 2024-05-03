import 'package:sav/common/utils/string.extension.dart';

class BaseData {
  static String splitCode = " | ";

  static int stringToInt(dynamic number) {
    if (number == null) {
      return 0;
    }
    if (number is int) {
      return number;
    }
    return number.toString().trim().toInt();
  }

  static int boolToInt(bool value) => (value != null)
      ? (value)
          ? 1
          : 0
      : 0;

  static bool intToBool(dynamic value) {
    if (value is bool) {
      return value;
    }
    if (value is int) {
      return (value != null) ? value == 1 : false;
    }
    return false;
  }

  static String? intListToString(List<int> values) {
    if (values == null) return null;

    String? result;

    int index = 0;
    values.forEach((element) {
      if (index == values.length)
        result = "$result + $element";
      else
        result = "$result + $element + $splitCode";

      index++;
    });

    return result;
  }

  static List<int>? stringToIntList(String value) {
    List<int> result = [];

    if (value == null) return null;

    var splitted = value.split(splitCode);
    splitted.forEach((element) {
      result.add(element.toInt());
    });

    return result;
  }

  static String? stringListToString(List<String> values) {
    if (values == null) return null;

    String? result;

    int index = 0;
    values.forEach((element) {
      if (index == values.length)
        result = "$result + $element";
      else
        result = "$result + $element + $splitCode";

      index++;
    });

    return result;
  }

  static List<String>? stringToStringList(String value) {
    List<String> result = [];

    if (value == null) return null;

    var splitted = value.split(splitCode);
    splitted.forEach((element) {
      result.add(element);
    });

    return result;
  }
}
