class BaseResponseDto {
  int statusCode = 0;
  bool status = false;
  String message = "";

  bool get succes => statusCode == 200 || statusCode == 201;

  bool get isUnauthorized => statusCode == 401;

  BaseResponseDto({
    this.statusCode = 200,
    this.status = true,
    this.message = ""
  });

  BaseResponseDto.fromJson(Map<String, dynamic> json) {
    try {
      if (json != null) {
          statusCode = json["status_code"];
          status = json["status"];
          message =  json["message"];
      } else
        BaseResponseDto();
    } catch (e) {
      BaseResponseDto();
    }
  }

  Map<String, dynamic> toJson() => <String, dynamic>{
    'status_code': statusCode,
    'status': status,
    'message': message
  };

  dynamic getData(json) {
    if (json != null) {
      var jsonData = json["data"];
      if (jsonData is dynamic) {
        return jsonData;
      }
    }
    return null;
  }
}
