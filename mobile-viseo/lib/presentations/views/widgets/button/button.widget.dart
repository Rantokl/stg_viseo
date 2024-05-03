import 'package:flutter/material.dart';
import 'package:sav/common/theme/theme.utils.dart';

class ButtonWidgets {
  static Widget buildButton({
    required String label,
        required Color background,
        required void Function()? onPressed
      }) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
          padding: EdgeInsets.all(ThemeSpacing.ml),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(ThemeSpacing.sm), // <-- Radius
          ),
          backgroundColor: background,
          textStyle: body.copyWith(
              color: ThemeColors.white, fontSize: ThemeSpacing.m)),
      child: Text(label.toUpperCase()),
    );
  }
}