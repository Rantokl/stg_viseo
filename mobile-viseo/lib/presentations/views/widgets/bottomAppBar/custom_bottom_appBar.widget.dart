
import 'package:flutter_svg/flutter_svg.dart';
import 'package:flutter/material.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/presentations/views/widgets/bottomAppBar/navigation_item.widget.dart';

Widget CustomBottomAppBar() {
  return BottomAppBar(
      height: 80,
      color: ThemeColors.background,
      child: Padding(
        padding: EdgeInsets.only(bottom: 10),
        child: NavigationItem(),
      )
  );
}