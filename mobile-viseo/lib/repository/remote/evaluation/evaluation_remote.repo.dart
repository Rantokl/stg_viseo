import 'package:sav/models/constant/urls.dart';
import 'package:sav/models/dto/devis/type_devis_response.dto.dart';
import 'package:sav/models/dto/evaluation/question_response.dto.dart';
import 'package:sav/models/dto/evaluation/list_question_result.dto.dart';
import 'package:sav/models/dto/evaluation/question_result.dto.dart';
import 'package:sav/models/dto/evaluation/evaluation_response.dto.dart';
import 'package:sav/models/dto/panic/panic_response.dto.dart';
import 'package:sav/models/dto/panic/send_panic_response.dto.dart';
import 'package:sav/repository/remote/base_remote.bdl.dart';

class EvaluationRemoteRepo {
  BaseRemoteBDL get helper => BaseRemoteBDL();

  Future<QuestionResponseDto> getEvaluation() async {
    var response = await helper.get(
      "${Urls.evaluation.evaluation}/",
    );   
    return QuestionResponseDto.fromJson(response);
  }

  Future<EvaluationResponseDto> postPrestation(ListQuestionResultDto request) async {
    print("========request ${request.toJsonLocal()}");
    var response = await helper.post(
        "${Urls.evaluation.prestation}/",
        body: request.toJsonLocal()
    );
    print("======response $response");
    return EvaluationResponseDto.fromJson(response);
  }

}