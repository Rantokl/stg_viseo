import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';


class CustomModal {
 static Widget simpleModal({Widget? icon, required String title, String? description, required VoidCallback onPressed}) {
  return AlertDialog(
    backgroundColor: ThemeColors.dark,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(10.0),
    ),
    title: icon,
    content: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          title,
          style: TextStyle(color: ThemeColors.white, fontWeight: FontWeight.bold, height: 1.5),
          textAlign: TextAlign.center,
        ),
        if (description != null)
          Padding(
            padding: const EdgeInsets.only(top: 10),
            child: Text(
              description,
              style: TextStyle(color: ThemeColors.white, height: 1.5),
              textAlign: TextAlign.center,
            ),
          )
      ],
    ),
    actions: <Widget>[
      Padding(
        padding: EdgeInsets.only(bottom: 10, left: 20, right: 20),
        child: CustomeButton.elevated(
        fontSize: ThemeSpacing.m,
        buttonTitle: "OK",
        onPressed: onPressed,
        color: ThemeColors.green,
      ),
      )
    ],
  );
}


static Widget AvisModal({
  required BuildContext context, required Widget icon, required Widget child,required VoidCallback onPressedYes, required VoidCallback onPressedNo}) {

  var _screenWidth = MediaQuery.of(context).size.width;

  return AlertDialog(
    backgroundColor: ThemeColors.dark,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(10.0),
    ),
    title: icon,
    content: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        child,
      ],
    ),
    actions: <Widget> [
      Padding(
        padding: EdgeInsets.only(bottom: 10, left: 20, right: 20),
        child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              CustomeButton.elevated(
                fontSize: ThemeSpacing.m,
                buttonTitle: "NON",
                onPressed: onPressedNo,
                color: ThemeColors.gray,
              ),
              CustomeButton.elevated(
                fontSize: ThemeSpacing.m,
                buttonTitle: "OUI",
                onPressed: onPressedYes,
                color: ThemeColors.green,
              ),
            ],
          )      
        )
    ],
  );
}

static Widget twoActionModal({
  required BuildContext context, 
  required Widget icon, 
  required Widget child, 
  required String firstActionName,
  required VoidCallback onFirstActionPressed, 
  required String secondActionName, 
  required VoidCallback onSecondActionPressed,
  double? fontSize
  }) {

  var _screenWidth = MediaQuery.of(context).size.width;

  return AlertDialog(
    backgroundColor: ThemeColors.dark,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(10.0),
    ),
    title: icon,
    content: Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.center,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        child,
      ],
    ),
    actions: <Widget> [
      Padding(
        padding: EdgeInsets.only(bottom: 10, left: 20, right: 20),
        child: Row(
            // mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              CustomeButton.elevated(
                fontSize: fontSize == null ? ThemeSpacing.m : fontSize,
                buttonTitle: firstActionName,
                onPressed: onFirstActionPressed,
                color: ThemeColors.gray,
                isRow: true
              ),
              HorizontalSpace.m,
              CustomeButton.elevated(
                fontSize: fontSize == null ? ThemeSpacing.m : fontSize,
                buttonTitle: secondActionName,
                onPressed: onSecondActionPressed,
                color: ThemeColors.green,
                isRow: true
              ),
            ],
          )      
        )
    ],
  );
}


}