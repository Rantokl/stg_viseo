import 'package:flutter/material.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/values/strings.dart';

class InputWidgets {
  static Widget buildTextField({
    Key? key,
    Widget? prefixIcon,
    String? label,
    String? hintText,
    String? initialValue,
    TextInputType? inputType,
    bool isRequired = false,
    String? Function(String?)? validator,
    required void Function(String) onValidField,
    void Function(String)? onChange,
  }) {
    return TextFormField(
      key: key,
      initialValue: initialValue,
      style: TextStyle(color: ThemeColors.dark),
      decoration: InputDecoration(
          filled: true,
          fillColor: ThemeColors.gray,
          prefixIcon: prefixIcon,
          hintText: hintText,
          labelText: label,
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(ThemeSpacing.s),
            borderSide: BorderSide(
                width: ThemeSpacing.xxs,
                color: ThemeColors.neutral60), //<-- SEE HERE
          )),
      keyboardType: inputType,
      //autovalidateMode: AutovalidateMode.onUserInteraction,
      validator: validator ??
              (value) {
            if (isRequired) {
              if (value == null || value.isEmpty) {
                return Strings.common.fieldRequired;
              }
            }
            onValidField(value ?? "");
            return null;
          },
      onChanged: onChange,
      scrollPadding: EdgeInsets.all(ThemeSpacing.xxl3),
    );
  }

  static Widget buildPasswordField({
    Key? key,
    String? label,
    String? hintText,
    required bool isPasswordHidden,
    required void Function(String) onValidPassword,
    required void Function(bool) onVisibilityChange,
    void Function(String)? onChange,
  }) {
    return TextFormField(
      key: key,
      style: TextStyle(color: ThemeColors.dark),
      decoration: InputDecoration(
          filled: true,
          fillColor: ThemeColors.gray,
          hintText: hintText,
          labelText: label,
          prefixIcon: Icon(
            Icons.lock,
            color: ThemeColors.neutral40,
          ),
          suffixIcon: passwordSuffix(isPasswordHidden, onVisibilityChange),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(ThemeSpacing.s),
            borderSide: BorderSide(
                width: ThemeSpacing.xxs,
                color: ThemeColors.neutral60), //<-- SEE HERE
          )),
      keyboardType: TextInputType.visiblePassword,
      obscureText: !isPasswordHidden,
      //autovalidateMode: AutovalidateMode.onUserInteraction,
      validator: (value) {
        if (value!.isEmpty) {
          return Strings.common.passwordRequired;
        }
        onValidPassword(value);
        return null;
      },
      onChanged: onChange,
      scrollPadding: EdgeInsets.all(ThemeSpacing.xxl3),
    );
  }

  static Widget passwordSuffix(
      bool isPasswordHidden,
      void Function(bool) onVisibilityChange,
      ) {
    return IconButton(
      icon: Icon(
        isPasswordHidden ? Icons.visibility : Icons.visibility_off,
        color: ThemeColors.black,
      ),
      onPressed: () => onVisibilityChange(!isPasswordHidden),
    );
  }
}