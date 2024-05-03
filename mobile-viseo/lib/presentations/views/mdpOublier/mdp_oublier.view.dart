import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/mdpOublier/mdp_oublier.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/button.widget.dart';
import 'package:sav/presentations/views/widgets/input/input.widget.dart';

class MdpOublierView extends BaseStatelessView<MdpOublierController> {
  final _formKey = GlobalKey<FormState>();
  late double _screenWidth;
  late double _screenHeight;

  MdpOublierView({Key? key})
      : super(key: key, controller: Get.put(MdpOublierController())) {}

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
            body: ListView(
              physics: ScrollPhysics(), 
              children: [
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
                                    ]
                                )
                            )
                          ]
                      )
                  )
                ]
            )
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
            )
        ));
  }

  Widget _buildForm() {
    return Container(
      width: _screenWidth,
      child: Column(
        children: [
          VerticalSpace.xl,
          Text(
            Strings.mdpOublier.instruction,
            style: TextStyle(color: ThemeColors.white, fontWeight: FontWeight.bold, fontSize: ThemeSpacing.m, height: 1.5),
            textAlign: TextAlign.center,
          ),
          VerticalSpace.xl,
          InputWidgets.buildTextField(
            prefixIcon: Icon(
              Icons.person_outlined,
              color: ThemeColors.neutral40,
            ),
            hintText: Strings.login.email,
            inputType: TextInputType.emailAddress,
            isRequired: true,
            validator: controller.mailValidator,
            onValidField: controller.onValidEmail,
          ),
          VerticalSpace.xl,
          SafeArea(
            child: Container(
              width: _screenWidth - ThemeSpacing.xl * 2,
              padding: EdgeInsets.symmetric(vertical: ThemeSpacing.m),
              child: ButtonWidgets.buildButton(
                  label: Strings.mdpOublier.envoyer,
                  background: ThemeColors.dark,
                  onPressed: _onSubmit
              ),
            ),
          )
        ],
      ),
    );
  }

  _onSubmit() {
    if (_formKey.currentState!.validate()) {
      controller.postEmail(
      success: (isSucces) {
        if (isSucces) {
          showToast(title: Strings.mdpOublier.titre, message: Strings.mdpOublier.description);
          pushNamed(routeName: Routes.login, addToBack: false);
        } else {
          showErrorDialog(title: Strings.mdpOublier.error, message: controller.messageResponse.value);
        }
      },
      failure: (message){
        showErrorDialog(title: Strings.login.title, message: message);
      });
    }
  }
}
