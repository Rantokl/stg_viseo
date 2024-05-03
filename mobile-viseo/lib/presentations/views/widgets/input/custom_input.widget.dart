import 'package:flutter/material.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/values/strings.dart';

Widget CustomInput({
  required int line, 
  TextEditingController? controller, 
  String? label, 
  Icon? icon, 
  Widget? suffixIcon,
  bool isRequired = true
  }) {
  return  TextFormField(
      controller: controller,
      maxLines: line,
      decoration: InputDecoration(
        fillColor: ThemeColors.gray,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide.none,
        ),
        labelText: label,
        prefixIcon:  icon != null ? Icon(icon!.icon) : null,
        suffixIcon: suffixIcon,
        filled: true,
        alignLabelWithHint: true,
        floatingLabelBehavior: FloatingLabelBehavior.never,
      ),
      validator: (value) {
            if (isRequired) {
              if (value == null || value.isEmpty || value.trim().isEmpty) {
                return Strings.common.fieldRequired;
              }
            }
            return null;
          },
  );
}