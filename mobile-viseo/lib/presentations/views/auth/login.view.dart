import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/auth/login.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/main.view.dart';
import 'package:sav/presentations/views/widgets/button/button.widget.dart';
import 'package:sav/presentations/views/widgets/input/input.widget.dart';

class LoginView extends BaseStatelessView<LoginController> {
  final _formKey = GlobalKey<FormState>();
  late double _screenWidth;
  late double _screenHeight;

  LoginView({Key? key})
      : super(key: key, controller: Get.put(LoginController())) {}

  @override
  Widget build(BuildContext context) {
    _screenWidth = MediaQuery.of(context).size.width;
    _screenHeight = MediaQuery.of(context).size.height;

    return Form(
        key: _formKey,
        child: Scaffold(
            appBar: AppBar(
              backgroundColor: ThemeColors.background,
              systemOverlayStyle: SystemUiOverlayStyle.dark,
              elevation: 0,
              toolbarHeight: 0,
            ),
            body: Obx(() => ListView(physics: ScrollPhysics(), children: [
                  Padding(
                      padding: EdgeInsets.all(ThemeSpacing.xl),
                      child: Column(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Container(
                                child: Column(
                                    children: [
                                      _buildLogo(),
                                      _buildForm(),
                                      VerticalSpace.xl,
                                      _buildPasswordLink()
                                    ]
                                )
                            )
                          ]
                      )
                  )
                ]
            ))
        )
    );
  }

  Widget _buildLogo() {
    return Container(
        padding: EdgeInsets.all(ThemeSpacing.xl),
        width: _screenWidth,
        height: _screenHeight / 3,
        child: Center(
            child: Image.asset(
          Assets.logo,
          fit: BoxFit.fitWidth,
        )));
  }

  Widget _buildForm() {
    return Container(
      width: _screenWidth,
      child: Column(
        children: [
          VerticalSpace.xl,
          InputWidgets.buildTextField(
            prefixIcon: Icon(
              Icons.person_outlined,
              color: ThemeColors.neutral40,
            ),
            hintText: Strings.login.username,
            inputType: TextInputType.emailAddress,
            isRequired: true,
            validator: controller.usernameValidator,
            onValidField: controller.onValidUserName,
          ),
          VerticalSpace.xl,
          InputWidgets.buildPasswordField(
            hintText: Strings.login.password,
            onVisibilityChange: (nowHidden) {
              controller.onPasswordVisibilityChange(nowHidden);
            },
            isPasswordHidden: controller.isPasswordHidden.value,
            onValidPassword: controller.onValidPassword,
          ),
          VerticalSpace.xl,
          SafeArea(
            child: Container(
              width: _screenWidth - ThemeSpacing.xl * 2,
              padding: EdgeInsets.symmetric(vertical: ThemeSpacing.m),
              child: ButtonWidgets.buildButton(
                  label: Strings.login.submit,
                  background: ThemeColors.dark,
                  onPressed: _onSubmit
              ),
            ),
          )
        ],
      ),
    );
  }

  Widget _buildPasswordLink(){
    return Center(
      child: RichText(
          text: TextSpan(
              text: Strings.login.forgottenPassword,
              style: bodyS.copyWith(color: ThemeColors.gray),
              recognizer: new TapGestureRecognizer()
                ..onTap = () {
                pushNamed(routeName: Routes.mdpOublier);
                }
          )
      ),
    );
  }


  _onSubmit() async {
    if (_formKey.currentState!.validate()) {
      controller.authenticate(success: (isSucces) {
        if (isSucces) {
          if (controller.prefs.profile!.isAdmin){
            Get.offAllNamed(Routes.chatAdmin);
          }
          else {
            Get.offAllNamed(Routes.main);
          }
        }
      },
      failure: (message){
        showErrorDialog(title: Strings.login.title, message: message);
      });
    }
  }
}
