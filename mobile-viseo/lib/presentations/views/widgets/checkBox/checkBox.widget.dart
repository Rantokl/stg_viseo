import 'package:flutter/material.dart';
import 'package:sav/common/theme/theme.utils.dart';

class CheckBoxWidget extends StatelessWidget{
  final int item_id;
  final int id;
  final bool isCheck;
  final Function onChange;

  const CheckBoxWidget({Key? key,
    required this.item_id,
    required this.id,
    required this.isCheck,
    required this.onChange
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    Color getColor(Set<MaterialState> states) {
      const Set<MaterialState> interactiveStates = <MaterialState>{
        MaterialState.selected
      };
      if (states.any(interactiveStates.contains)) {
        return ThemeColors.green;
      }
      return Colors.white;
    }
    // TODO: implement build
    return Checkbox(
      value: isCheck,
      onChanged: (bool? value){
        onChange(item_id, id);
      },
      fillColor: MaterialStateProperty.resolveWith(getColor),
    );
  }
}