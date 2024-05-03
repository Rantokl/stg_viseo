import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/contact/contact.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/card/custom_card.widget.dart';

class ContactView extends BaseStatelessView<ContactController> {

  ContactView({
    Key? key,
  }) : super(key: key, controller: Get.put(ContactController())) {
    WidgetsBinding.instance!.addPostFrameCallback((_) {
      controller.getContact(
          success: (success) {

          },
          failure: (response) {
            if (response.statusCode == Strings.common.expiredTokenCode){
              showTokenExpiredModal();
            }
          }
      );
    });
  }

  List<Color> headerColors = [
    ThemeColors.blue,
    ThemeColors.yellow,
    ThemeColors.green,
    ThemeColors.neutral40,
  ];

  @override
  Widget build(BuildContext context) {
    return baseScaffoldView(
      appBarController: AppBarController(
        title: Strings.contact.title,
      ),
      body: Obx(
            () => (controller.isLoading)
            ? Container()
            : controller.contact.value == null ?
        Expanded(
          child: Container(
            alignment: Alignment.center, // Center the text both vertically and horizontally
            child: Text(
              Strings.contact.noData,
              style: TextStyle(color: ThemeColors.white),
            ),
          ),
        ) :
        Expanded(
          child: SingleChildScrollView(
            child: ListView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              itemCount: controller.contact.value!.data.length,
              itemBuilder: (context, index) {
                var contact = controller.contact.value!.data[index];
                return Padding(
                  padding: EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                  child: CustomCard.Contact(
                      title: Strings.contact.contactTitle,
                      description: contact.nom ?? '',
                      enteteColor: headerColors[0],
                      items: [
                        ContactItem(icon: Icons.phone, text: contact.telephone ?? ''),
                        ContactItem(icon: Icons.location_on_sharp, text: contact.siege ?? ''),
                      ]
                  ),
                );
              },
            ),
          ),
        ),
      ),
    );
  }
}
