import 'package:flutter/material.dart';
import 'package:sav/common/utils/app.utils.dart';

class AppTheme {
  static buildTheme() {
    final ThemeData base = ThemeData.light();
    return ThemeData(
        primaryColor: ThemeColors.primary,
        primaryColorLight: ThemeColors.primary,
        primaryColorDark: ThemeColors.primary,
        scaffoldBackgroundColor: ThemeColors.background,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        appBarTheme: AppBarTheme(color: ThemeColors.primary),
        textTheme: base.textTheme.copyWith().apply(fontFamily: fontFamily),
        colorScheme: ColorScheme.fromSwatch()
            .copyWith(secondary: ThemeColors.secondary)
            .copyWith(error: ThemeColors.error));
  }
}

class ThemeColors {
  static const white = Color(0xFFFFFFFF);
  static const black = Color(0xFF000000);
  static const blackTheme = Color(0xFF121212);
  static const dark = Color(0xFF343434);
  static const dark01 = Color.fromARGB(255, 77, 77, 77);
  static const red = Color(0xFFFF0000);
  static const yellow = Color(0xFFFFD402);
  static const blue = Color(0xFF39A7DF);
  static const orange = Color(0xFFE95A0C);
  static const gray = Color(0xFFAEAEAE);
  static const green = Color(0xFF3EAB36);
  static const neutral60 = Color(0xFFD6D6D6);
  static const neutral40 = Color(0xFF878787);
  static const iconDialog = Color(0xFF4CAF50);
  static const transparent = Color(0xFFFFFF);

  static Color get primary => dark;

  static Color get primaryVariant => dark;

  static Color get secondary => green;

  static Color get secondaryVariant => green;

  static Color get background => blackTheme;

  static Color get surface => blackTheme;

  static Color get error => red;

  static Color get onPrimary => gray;

  static Color get onSecondary => white;

  static Color get onBackground => gray;

  static Color get onSurface => gray;

  static Color get onError => white;
}

const totalWidthLimit = 720;
const totalHeightLimt = 2290;

class ThemeSize {
  static bool isSmallScreen(BuildContext context) {
    /*return MediaQuery.of(context)
        .map((mq) => mq.size.width * mq.devicePixelRatio < totalWidthLimit);*/
    return MediaQuery.of(context)
        .map((mq) => mq.size.height * mq.devicePixelRatio < totalHeightLimt);
  }

  static const double xxl = 100;
}

class ThemeSpacing {
  static const double xxxs = 1.0;
  static const double xxs = 2.0;
  static const double xs = 4.0;
  static const double s = 8.0;
  static const double sm = 12.0;
  static const double m = 16.0;
  static const double ml = 18.0;
  static const double l = 24.0;
  static const double xl = 32.0;
  static const double xxl = 44.0;
  static const double xxl2 = 64.0;
  static const double xxl3 = 128.0;
}

/// Sized spaces for vertical layouts such as Column
class VerticalSpace {
  static SizedBox _widget(double height) => SizedBox(height: height);

  static final SizedBox xs = _widget(ThemeSpacing.xs);

  static final SizedBox s = _widget(ThemeSpacing.s);

  static final SizedBox sm = _widget(ThemeSpacing.sm);

  static final SizedBox m = _widget(ThemeSpacing.m);

  static final SizedBox l = _widget(ThemeSpacing.l);

  static final SizedBox xl = _widget(ThemeSpacing.xl);

  static final SizedBox xxl = _widget(ThemeSpacing.xxl);

  static final SizedBox xxl2 = _widget(ThemeSpacing.xxl2);

  static final SizedBox xxl3 = _widget(ThemeSpacing.xxl3);

  static SizedBox biggestSpace(bool isSmallScreen) =>
      _widget(isSmallScreen ? ThemeSpacing.xl : ThemeSpacing.xxl3);
}

/// Sized spaces for horizontal layouts such as Row
class HorizontalSpace {
  static SizedBox _widget(double width) => SizedBox(width: width);

  static final SizedBox xs = _widget(ThemeSpacing.xs);

  static final SizedBox s = _widget(ThemeSpacing.s);

  static final SizedBox sm = _widget(ThemeSpacing.sm);

  static final SizedBox m = _widget(ThemeSpacing.m);

  static final SizedBox l = _widget(ThemeSpacing.l);

  static final SizedBox xl = _widget(ThemeSpacing.xl);

  static final SizedBox xxl = _widget(ThemeSpacing.xxl);

  static final SizedBox xxl2 = _widget(ThemeSpacing.xxl2);

  static final SizedBox xxl3 = _widget(ThemeSpacing.xxl3);
}

class ThemeBorder {
  static BorderRadius _border(double size) => BorderRadius.circular(size);

  static final BorderRadius xsRoundedBorder = _border(ThemeSpacing.xs);

  static final BorderRadius sRoundedBorder = _border(ThemeSpacing.s);

  static final BorderRadius smRoundedBorder = _border(ThemeSpacing.sm);

  static final BorderRadius mRoundedBorder = _border(ThemeSpacing.m);

  static final BorderRadius mlRoundedBorder = _border(ThemeSpacing.ml);

  static final BorderRadius lRoundedBorder = _border(ThemeSpacing.l);

  static final BorderRadius xlRoundedBorder = _border(ThemeSpacing.xl);
}

final String fontFamily = 'Inter';
const defaultTextHeightFactor = 1.5;

final TextStyle _body = TextStyle(
  fontFamily: fontFamily,
  fontWeight: FontWeight.w500,
  height: 1.5,
);

final TextStyle title1 = _body.copyWith(height: 1.0, fontSize: 36);

final TextStyle title2 = _body.copyWith(height: 1.0, fontSize: 28);

final TextStyle body = bodyM;

final TextStyle bodyXxs = _body.copyWith(fontSize: 10);

final TextStyle bodyXs = _body.copyWith(fontSize: 12);

final TextStyle bodyS = _body.copyWith(fontSize: 14);

final TextStyle bodyM = _body.copyWith(fontSize: 16);

final TextStyle bodyL = _body.copyWith(fontSize: 18);

final TextStyle bodyXl = _body.copyWith(fontSize: 20);

final TextStyle bodyXxl = _body.copyWith(fontSize: 22);

extension TextStyleVariants on TextStyle {
  TextStyle bold() {
    return copyWith(fontWeight: FontWeight.bold);
  }

  TextStyle underline() {
    return copyWith(decoration: TextDecoration.underline);
  }
}
