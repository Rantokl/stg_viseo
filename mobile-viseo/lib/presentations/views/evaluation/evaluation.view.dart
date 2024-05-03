import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/evaluation/evaluation.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';
import 'package:sav/presentations/views/widgets/input/custom_input.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';

class EvaluationView extends BaseStatelessView<EvaluationController> {

  EvaluationView({
    Key? key,
  }) : super(key: key, controller: Get.put(EvaluationController())) {}

  late double _screenWidth;
  late double _screenHeight;
  final TextEditingController comment = TextEditingController();
  @override
  Widget build(BuildContext context) {

    List text = [
      {
        "text": Strings.evaluation.question,
        "size": 20.0,
        "isBold": true
      },
      {
        "text" : Strings.evaluation.note
      }
    ];

    _screenWidth = MediaQuery.of(context).size.width;
    _screenHeight = MediaQuery.of(context).size.height;

    void postEvaluation() async {
      controller.evaluation.value.commentaire = comment.text;
      await controller.postEvaluation(
        success: (isSucces) {
          Get.dialog(
            CustomModal.simpleModal(
              icon: SvgPicture.asset(Assets.icons.check, height: 20,),
              title: Strings.evaluation.modalTitle, 
              description: Strings.evaluation.modalDescription,
              onPressed: () {
                Get.back();
                Get.back();
              }
            )
          );
        },
        failure: (isfailure) {
          showErrorDialog(title: Strings.evaluation.error, message: controller.messagaResponseEvaluation);
        }
      );
    }
   
    return baseScaffoldView(
      appBarController: AppBarController(
        title: Strings.evaluation.title,
      ),
      body: Obx(() => controller.isLoading
              ? Container()
              : Expanded(
                child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: 20),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        IndexedStack(
                          alignment: Alignment.center,
                          index: controller.questionIndex.value,
                          children: [
                            ...controller.question.value!.data.map((question) => 
                              Column(
                                children: [
                                  Text(
                                    "Question ${question.id - controller.questionNumero.value + 1}",
                                    style: TextStyle(color: ThemeColors.white, fontWeight: FontWeight.bold, fontSize: 30.0),
                                    textAlign: TextAlign.center,
                                  ),
                                  VerticalSpace.m,
                                  Text(question.question_evaluation, style: TextStyle(color: ThemeColors.white), textAlign: TextAlign.center,),
                                ],
                              )
                            ),
                            Column(
                              children: [
                                Text(
                                  Strings.evaluation.comment,
                                  style: TextStyle(color: ThemeColors.white, fontWeight: FontWeight.bold),
                                  textAlign: TextAlign.center,
                                ),
                                VerticalSpace.m,
                                CustomInput(line: 10, label: Strings.evaluation.addComment, controller: comment, isRequired: false),
                                VerticalSpace.m,
                              ],
                            ),
                          ],
                        ),
                        controller.isQuestionFinished.isFalse
                        ? Column(
                            children: [
                              _moodRating(),
                              VerticalSpace.l,
                              CustomeButton.elevated(
                                fontSize: ThemeSpacing.m,
                                buttonTitle: Strings.evaluation.next,
                                onPressed: () => controller.changeQuestionIndex(), 
                                color: ThemeColors.green
                              )
                            ],
                        )
                        : CustomeButton.elevated(
                              fontSize: ThemeSpacing.m,
                              buttonTitle: Strings.evaluation.send,
                              onPressed: () => postEvaluation(), 
                              color: ThemeColors.green
                          ),
                      ],
                    ),
                  ),
              )
      )
    );
  }

  Widget _moodRating() {
  final List<String> moods = ['🤩', '😊', '😐', '🙁']; 
  return Column(
    children: [
      Text(controller.mood.value, style: TextStyle(color: ThemeColors.yellow, fontWeight: FontWeight.bold)),
      Row(
        mainAxisSize: MainAxisSize.min,
        children: List.generate(4, (index) {
          return GestureDetector(
            onTap: () {
              controller.changeRate(index);
            },
            child: Container(
              margin: EdgeInsets.all(10.0),
              padding: EdgeInsets.all(10.0),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(20.0),
                color: index == controller.rateIndex.value ? ThemeColors.yellow : ThemeColors.dark, 
              ),
              child: Text(
                moods[index],
                style: TextStyle(fontSize: 24.0),
              ),
            ),
          );
        }),
      ),
    ],
  );
}

}


