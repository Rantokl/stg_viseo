import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/dto/evaluation/list_question_result.dto.dart';
import 'package:sav/models/dto/evaluation/question_response.dto.dart';
import 'package:sav/models/dto/evaluation/question_result.dto.dart';
import 'package:sav/presentations/controllers/base.controller.dart';
import 'package:sav/services/applying/remote/evaluation/evaluation_remote.SA.dart';

class EvaluationController extends BaseController {
  
  var rateIndex  = 0.obs;
  var mood = "Très bien".obs;
  var questionIndex = 0.obs;
  var questionNumero = 0.obs;

  late EvaluationRemoteSA serviceEvaluation;
  Rx<QuestionResponseDto?> question= Rx<QuestionResponseDto?>(null);
  var evaluation = ListQuestionResultDto(questions: [], commentaire: "").obs;
  var messagaResponseEvaluation = "";
  var isQuestionFinished = false.obs;
  
  @override
  onInit() {
    super.onInit();
    this.serviceEvaluation = EvaluationRemoteSA();
  }

  @override
  void onReady() {
    super.onReady();
    getEvaluation();
  }

  Future<void> changeRate(int index) async {
    rateIndex.value = index;
    // questionResult.value.note_evaluation = rateIndex.value + 1;
    // print("======= ${questionResult.value.note_evaluation}");
    switch (index) {
      case 0:
        mood.value = "Très bien";
        break;
      case 1:
        mood.value = "Bien";
        break;
      case 2:
        mood.value = "Mauvais";
        break;
      case 3:
        mood.value = "Très mauvais";
        break;
      default:
    }
  }

  // void changeQuestionIndex() {
  //   if (questionIndex < question.value!.data.length - 1){
      
  //     questionResult.value.question_id = questionIndex.value + 9;
  //     print("======= ${questionResult.value.toJsonLocal()}");
  //     evaluation.value.questions.add(questionResult.value);
  //     print("======= ${evaluation.value.toJsonLocal()}");
  //     questionIndex.value += 1;
  //     // questionResult.value.note_evaluation = 1;
  //     // questionResult.value.question_id = 0;
  //     // rateIndex.value = 0;
  //   } else {
        
  //       questionResult.value.question_id = questionIndex.value + 9;
  //       print("======= ${questionResult.value.toJsonLocal()}");
  //       evaluation.value.questions.add(questionResult.value);
  //       print("======= ${evaluation.value.toJsonLocal()}");
  //       questionIndex.value += 1;
  //       isQuestionFinished.value = true;
      
  //   }  
  // }

  void changeQuestionIndex() {
  if (questionIndex < question.value!.data.length - 1) {
    var newQuestionResult = QuestionResultDto(question_id: questionIndex.value + questionNumero.value, note_id: rateIndex.value + 1);
    print("======= ${newQuestionResult.toJsonLocal()}");
    evaluation.value.questions.add(newQuestionResult);
    print("======= ${evaluation.value.toJsonLocal()}");
    questionIndex.value += 1;
    rateIndex.value = 0;
    mood.value = "Très bien";
  } else {
    var newQuestionResult = QuestionResultDto(question_id: questionIndex.value + questionNumero.value, note_id: rateIndex.value + 1);
    print("======= ${newQuestionResult.toJsonLocal()}");
    evaluation.value.questions.add(newQuestionResult);
    print("======= ${evaluation.value.toJsonLocal()}");
    questionIndex.value += 1;
    rateIndex.value = 0;
    mood.value = "Très bien";
    isQuestionFinished.value = true;
  }
}


  getEvaluation() async {
    loading(true);
    await serviceEvaluation.getEvaluation(
      onSuccess: (response) {
        question.value = response;
        questionNumero.value = question.value!.data.first.id;
        loading(false);
      },
      onFailure: (error) {
        print(error);
        loading(false);
      },
    );
  }

  postEvaluation({
    required CompletionClosure<bool> success,
    CompletionClosure<String>? failure
  }) async {
    loading(true);
    await serviceEvaluation.postEvaluation(
      request: evaluation.value,
      onSuccess: (res) {
          print(res.message);
          messagaResponseEvaluation = res.message;
          loading(false);
          success.call(true);
        },
        onFailure: (message) {
          print(message);
          messagaResponseEvaluation = message;
          loading(false);
          failure?.call(message);
        }
    );
  }

}