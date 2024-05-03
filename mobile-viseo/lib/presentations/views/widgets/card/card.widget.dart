import 'package:flutter/cupertino.dart';
import 'package:sav/common/theme/theme.utils.dart';

class Cardwidgets {
  static Widget vehicleHeader ({
    required String number,
    required String model,
    required String specification
  }) {
    return Container(
      decoration: BoxDecoration(color: ThemeColors.gray),
      width: double.infinity,
      child: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              number,
              style: TextStyle(color: ThemeColors.dark, fontSize: 14, fontWeight: FontWeight.bold, decoration: TextDecoration.none),
            ),
            SizedBox(height: 10,),
            Text(
              model,
              style: TextStyle(color: ThemeColors.dark, fontSize: 14, fontWeight: FontWeight.bold, decoration: TextDecoration.none),
            ),
            SizedBox(height: 10),
            Text(
              specification,
              style: TextStyle(color: ThemeColors.dark, fontSize: 14, fontWeight: FontWeight.normal, decoration: TextDecoration.none),
            ),
          ],
        ),
      ),
    );
  }
}