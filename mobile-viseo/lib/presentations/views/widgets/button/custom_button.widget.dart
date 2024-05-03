import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:sav/common/theme/theme.utils.dart';


class CustomeButton {

  static Widget card({
    required VoidCallback? onPressed, 
    required String buttonTitle, 
    required Icon icon,
  }) {
    return Container(
      margin: EdgeInsets.symmetric(vertical: 3, horizontal: 3),
      child: ElevatedButton(
            onPressed: onPressed,
            style: ElevatedButton.styleFrom(
              backgroundColor: Color(ThemeColors.black.value),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15.0),
              ),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  child: Column(
                    children: [
                      icon,
                      Padding(
                        padding: const EdgeInsets.only(top: ThemeSpacing.s),
                        child: Text(
                          buttonTitle,
                          textAlign: TextAlign.center,
                          style: TextStyle(color: ThemeColors.gray),
                        ),
                      ),
                    ],
                  ),
                )
              ],
            ),
      ),
    );
  }

  static Widget dropDown<T>({
    required String? label, 
    T? selectedValue, 
    required List<T> item, 
    required Function(T?) changeItem,
    required String? Function(T?) validator,
    double? maxHeight,
    Icon? icon}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10.0),
      child: DropdownButtonFormField(
          menuMaxHeight: maxHeight,
          value: selectedValue,
          decoration: InputDecoration(
            border: OutlineInputBorder(borderSide: BorderSide(color: ThemeColors.transparent) ,borderRadius: const BorderRadius.all(Radius.circular(10.0))),
            hintText: label,
            filled: true,
            fillColor: ThemeColors.gray,
          ),
          style: const TextStyle(color: ThemeColors.dark),
          items: item.map<DropdownMenuItem<T>>((T value) {
            return DropdownMenuItem<T>(
              value: value,
              child: Text(value.toString()),
            );
          }).toList(),
          icon: icon,
          onChanged: changeItem,
          validator: validator,
      ),
    );
  }

  static Widget elevated({
  double vertical = 60.0,
  double? horizontal,
  required double fontSize,
  required VoidCallback onPressed,
  Color? color,
  required String buttonTitle,
  Icon? icon,
  bool isRow = false,
}) {
  final elevatedButton = ElevatedButton(
    onPressed: onPressed,
    style: ElevatedButton.styleFrom(
      fixedSize: Size(horizontal ?? double.infinity, vertical),
      backgroundColor: color ?? ThemeColors.green,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15.0),
      ),
    ),
    child: Center(
      child: Text(
        buttonTitle.toUpperCase(),
        style: TextStyle(
          color: Colors.white,
          fontSize: fontSize,
        ),
        softWrap: true,
        textAlign: TextAlign.center,
      ),
    ),
  );

  return isRow ? Expanded(child: elevatedButton) : elevatedButton;
}


  static Widget elevatedIcon({
    required double size,
    required double fontSize,
    required VoidCallback onPressed,
    Color? color,
    required String buttonTitle,
    Icon? icon,}) {
  return  ElevatedButton.icon(
          onPressed: onPressed,
          style: ElevatedButton.styleFrom(
            padding: EdgeInsets.symmetric(horizontal: size),
            backgroundColor: color != null ? color : ThemeColors.green,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15.0),
            ),
          ),
          icon: Icon(
                    icon!.icon,
                    size: 15,
                    color: Colors.white,
                  ),
          label: Text(
                buttonTitle.toUpperCase(),
                style: TextStyle(
                  color: Colors.white,
                  fontSize: fontSize,
                ),
              ),
      );
  }

  static Widget iconButton({
    Color? color, 
    String? buttonTitle,
    required Icon icon, 
    VoidCallback? onPressed, 
    bool? container}) {
  return Container(
      width: 40.0,
      height: 40.0,
      decoration: container == true ? BoxDecoration(
        color: color,
        border: Border.all(color: color!),
        borderRadius: BorderRadius.circular(8.0),
      ) : null,
      child: IconButton(
        onPressed: onPressed,
        icon: icon,
        color: Colors.white,
      ),
    );
  }



  static Widget simpleButton({
    double vertical = 64.0,
    required String buttonTitle,
    required double fontSize,
    VoidCallback? onPressed,
    Icon? icon,
    bool? isLoading = false,
    bool? isActive = false,
    bool? isDisable = false
  }){
    return Padding(
      padding: const EdgeInsets.only(bottom: 10.0, left: 0),
      child: SizedBox(
        height: vertical,
        width: double.infinity,
        child: ElevatedButton(
          onPressed: !isDisable! ? onPressed :() {},
            child: Row(
              children: [
                Text(
                  buttonTitle,
                  style: TextStyle(color: isActive! ? ThemeColors.dark : ThemeColors.dark01)
                  ),
                  Spacer(),
                  !isLoading! ? 
                  Icon(
                    icon!.icon,
                    size: 25,
                    color: ThemeColors.dark01,
                  ) :
                   CircularProgressIndicator(
                    color: ThemeColors.green,
                   )
              ],
            ),
          style: ElevatedButton.styleFrom(
            backgroundColor: ThemeColors.gray,
            shape: RoundedRectangleBorder(
              side: const BorderSide(
                width: 1, // thickness
                color: Color.fromARGB(141, 24, 23, 23)
              ),
              borderRadius: BorderRadius.circular(10.0) 
            )
          ),
        ),
      ),
    );
  }

}