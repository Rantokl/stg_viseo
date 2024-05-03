import 'package:dartz/dartz.dart';
import 'package:flutter/material.dart';

typedef VoidClosure = Function();
typedef Closure<T> = T Function(T);
typedef WidgetForDto<T> = Widget Function(T);
typedef CompletionClosure<T> = Function(T);
typedef ValidatorClosure<T> = String Function(T);

typedef T DataCreator<T>();

extension NullableUtils<T> on T? {
  bool get isNull => this == null;

  bool get isNotNull => this != null;
}

extension FunctionalExtension<T> on T {
  R map<R>(R Function(T value) fn) {
    return fn(this);
  }
}

extension NullableStringUtils on String? {
  bool get isNullOrEmpty => isNull || this!.isEmpty;

  bool get isNotNullOrEmpty => isNotNull && this!.isNotEmpty;

  String get orEmpty => isNotNull ? this! : '';

  String capitalize() {
    if (isNullOrEmpty) {
      return '';
    }

    return this![0].toUpperCase() + this!.substring(1);
  }

  String capitalizeWords() {
    if (isNullOrEmpty) {
      return '';
    }

    return this!
        .replaceAll(RegExp(' +'), ' ')
        .split(' ')
        .map((str) => str.capitalize())
        .join(' ');
  }
}

extension JsonUtils on Map<String, dynamic> {
  String? getString(String fieldName) => this[fieldName] as String?;

  DateTime? getDate(String fieldName) =>
      getString(fieldName)?.map(DateTime.parse);

  int? getInt(String fieldName) {
    return catching(() => this[fieldName] as int).fold(
          (dynamic _) => getString(fieldName)?.map(int.tryParse),
          (value) => value,
    );
  }

  /// Returns double value equivalent to given field.
  /// This method is smart and get extract a double from any of the fields:
  ///
  /// - a standard double type: {"adouble": 189.65}
  /// - an int type: {"adouble": 189} (will return double 189.0)
  /// - a double encoded as a string: {"adouble": "189.65"}
  /// - an int encoded as a string: {"adouble": "189"} (will return double 189.0)
  double? getDouble(String fieldName) {
    return catching(() => this[fieldName] as double?).fold(
          (dynamic _) => catching(() => getInt(fieldName)!.toDouble()).fold(
            (dynamic _) => getString(fieldName)?.map(double.tryParse),
            (value) => value,
      ),
          (value) => value,
    );
  }

  bool? getBool(String fieldName) {
    return catching(() => this[fieldName] as bool).fold(
          (dynamic _) =>
      getString(fieldName) == null ? null : getString(fieldName) == 'true',
          (value) => value,
    );
  }

  Iterable<T> getIterable<T>(String fieldName) =>
      (this[fieldName] as List<dynamic>? ?? <dynamic>[])
          .map((dynamic value) => value as T);

  Iterable<Map<String, dynamic>> getJsonArray(String fieldName) =>
      getIterable<Map<String, dynamic>>(fieldName);

  List<T> getList<T>(String fieldName) => getIterable<T>(fieldName).toList();
}