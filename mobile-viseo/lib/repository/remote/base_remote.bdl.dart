import 'dart:convert';
import 'dart:io';

import 'package:dio/dio.dart';
import 'package:sav/common/exceptions/remote.exception.dart';
import 'package:sav/common/utils/app.log.dart';
import 'package:sav/common/utils/string.extension.dart';
import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/base_response.dto.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:http/http.dart' as http;

class BaseRemoteBDL {
  PreferenceSA pref = PreferenceSA.instance;
  AppLog loger = AppLog.instance;

  String get baseUrl => Urls.base;

  static final BaseRemoteBDL _instance = BaseRemoteBDL._internal();

  factory BaseRemoteBDL() => _instance;

  BaseRemoteBDL._internal();

  static BaseRemoteBDL get instance => BaseRemoteBDL();

  Map<String, String> get headers {
    var token = pref.token;
    if (token.isNullOrEmpty()) {
      return {"Content-Type": "application/json; charset=utf-8"};
    }
    return {
      "Content-Type": "application/json; charset=utf-8",
      "Authorization": "Bearer $token"
    };
  }

  Map<String, String> get headersFormData {
    return {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"};
  }

  Map<String, String> get applicationJson {
    return {"Content-Type": "application/json; charset=utf-8"};
  }

  String paramsString(Map<String, String>? params) {
    if ((params == null) || (params.isEmpty)) {
      return "";
    }
    var result = "?";
    params.forEach((key, value) {
      result += "$key=$value&";
    });
    return result.substring(0, result.lastIndex());
  }

  Future<dynamic> get(String url, {
    Map<String, String>? params, bool tokenRequired: true
  }) async {
    var responseJson;
    try {
      var finalUrl = "$baseUrl$url${paramsString(params ?? null)}";
      loger.print(tag: "API GET", data: finalUrl);

      final response = await http.get(Uri.parse(finalUrl),
          headers: (tokenRequired) ? headers : applicationJson);
      responseJson = _returnResponse(response);
    } on SocketException {
      responseJson = RemoteException(remoteMessage: 'No Internet connection')
          .toBaseResponseDto()
          .toJson();
    } on Exception catch (e) {
      responseJson =
          RemoteException(remoteMessage: '$e').toBaseResponseDto().toJson();
    }
    return responseJson;
  }

  Future<dynamic> post(String url,{dynamic body,bool tokenRequired: true}) async {
    loger.print(tag: "API POST", data: baseUrl + url);
    loger.print(tag: "API BODY", data: jsonEncode(body));
    var responseJson;
    try {
      var json = jsonEncode(body);
      final response = await http.post(
          Uri.parse((baseUrl + url)),
          headers: (tokenRequired) ? headers : applicationJson,
          body: json
      );
      responseJson = _returnResponse(response);
    } on SocketException {
      responseJson = RemoteException(remoteMessage:'No Internet connection')
          .toBaseResponseDto()
          .toJson();
    } on Exception catch (e) {
      responseJson = RemoteException(remoteMessage:'$e')
          .toBaseResponseDto()
          .toJson();
    }
    return responseJson;
  }

  Future<dynamic> postFormData(String url, FormData body) async {
    loger.print(tag: "API POST", data: baseUrl + url);
    var finalUrl = '$baseUrl$url';
    print("URL = $finalUrl");
    var token = pref.token;
    var responseJson;
    try {
      var dio = new Dio();
      final response = await dio.post(
        finalUrl,
        options: Options(
          contentType: "multipart/form-data",
          headers : {"Authorization": "Bearer $token"},
        ),
        data: body,
      );
      responseJson = response.data;
      print("=========== response bdl : $response");

    } on Exception catch (e) {

      print("=========== error bdl : $e");
      responseJson = RemoteException(remoteMessage:'$e')
          .toBaseResponseDto()
          .toJson();
    }
    return responseJson;
  }

  Future<dynamic> put(String url, dynamic body) async {
    loger.print(tag: "API PUT", data: baseUrl + url);
    var responseJson;
    try {
      var json = jsonEncode(body);
      final response = await http.put(
          Uri.parse((baseUrl + url)),
          headers: headers,
          body: json
      );
      responseJson = _returnResponse(response);
    } on SocketException {
      responseJson = RemoteException(remoteMessage:'No Internet connection')
          .toBaseResponseDto()
          .toJson();
    } on Exception catch (e) {
      responseJson = RemoteException(remoteMessage:'$e')
          .toBaseResponseDto()
          .toJson();
    }
    return responseJson;
  }

  Future<dynamic> delete(String url, {Map<String, String>? params}) async {
    var responseJson;
    try {
      var finalUrl = "$baseUrl$url${paramsString(params)}";
      loger.print(tag: "API DELETE", data: finalUrl);
      final response = await http.delete(
          Uri.parse(finalUrl),
          headers: headers
      );
      responseJson = _returnResponse(response);
    } on SocketException {
      responseJson = RemoteException(remoteMessage:'No Internet connection')
          .toBaseResponseDto()
          .toJson();
    } on Exception catch (e) {
      responseJson = RemoteException(remoteMessage:'$e')
          .toBaseResponseDto()
          .toJson();
    }
    return responseJson;
  }

  Future<dynamic> upload(String url, {
    Map<String, String>? body,
    required File file,
    String fileField = "fileMobile"
  }) async {

    var responseJson;
    try {
      loger.print(tag: "API UPLOAD", data: (baseUrl + url));
      var uri = Uri.parse(baseUrl + url);

      var request = new http.MultipartRequest("POST", uri);

      body?.forEach((key, value) {
        request.fields[key] = value;
      });

      headers.forEach((key, value) {
        request.headers[key] = value;
      });

      var multipartFile = await http.MultipartFile
          .fromPath(fileField, file.path);

      request.files.add(multipartFile);

      var response = await request.send();
      var responseData = await response.stream.toBytes();
      var responseString = String.fromCharCodes(responseData);
      responseJson = jsonDecode(responseString);
    } on SocketException {
      responseJson = RemoteException(remoteMessage:'No Internet connection')
          .toBaseResponseDto()
          .toJson();
    } on Exception catch (e) {
      responseJson = RemoteException(remoteMessage:'$e')
          .toBaseResponseDto()
          .toJson();
    }
    return responseJson;
  }

}

dynamic _returnResponse(http.Response response) {
  AppLog.instance.print(tag: "API RESPONSE", data: response.body.toString());
  var responseJson = jsonDecode(utf8.decode(response.bodyBytes));
  // AppLog.instance.print(tag: "API RESPONSE", data: responseJson);
  switch (response.statusCode) {
    case 200:
      return responseJson;
    default:
      return RemoteException(
          remoteMessage: response.body.toString(),
          code: response.statusCode
      ).toBaseResponseDto().toJson();
  }
}
