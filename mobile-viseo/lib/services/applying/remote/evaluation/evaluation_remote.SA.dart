import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/evaluation/question_response.dto.dart';
import 'package:sav/models/dto/evaluation/list_question_result.dto.dart';
import 'package:sav/models/dto/evaluation/evaluation_response.dto.dart';
import 'package:sav/repository/remote/evaluation/evaluation_remote.repo.dart';
import 'package:sav/services/applying/remote/base_remote.sa.dart';


class EvaluationRemoteSA extends BaseRemoteSA {

  final repository = EvaluationRemoteRepo();

  getEvaluation ({
    required CompletionClosure<QuestionResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
     var response = await repository.getEvaluation();
     switch (response.succes) {
      case true:
        onSuccess.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

  postEvaluation ({
    required ListQuestionResultDto request,
    required CompletionClosure<EvaluationResponseDto> onSuccess,
    CompletionClosure<String>? onFailure
  }) async {
    var response = await repository.postPrestation(request);
     switch (response.succes) {
      case true:
        onSuccess?.call(response);
        break;
      default:
        onFailure?.call(response.message);
        break;
    }
  }

}