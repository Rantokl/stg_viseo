import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/chat/chat.controller.dart';
import 'package:sav/presentations/controllers/chat/chat_admin.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;

class ChatAdminView extends BaseStatelessView<ChatAdminController> {
  ChatAdminView({Key? key})
      : super(key: key, controller: Get.put(ChatAdminController()));

  void logout() async {
    await controller.logout(success: (isSuccess) {
      pushNamed(routeName: Routes.login, addToBack: false);
    });
  }

  @override
  Widget build(BuildContext context) {
    return baseScaffoldView(
        appBarController: AppBarController(
            title: Strings.chat.adminTitle,
            logout:  logout 
        ),
        body: Obx(() => controller.isLoading
            ? Container()
            : controller.discussions.isEmpty ?
              Expanded(
                child: Container(
                  alignment: Alignment.center, // Center the text both vertically and horizontally
                  child: Text(
                    "Aucune discussion",
                    style: TextStyle(color: ThemeColors.white),
                  ),
                ),
              ) :
        Expanded(
          child: SingleChildScrollView(
            child: ListView.builder(
                shrinkWrap: true,
                physics: NeverScrollableScrollPhysics(),
                itemCount: controller.discussions.length,
                itemBuilder: (context, index){
                  return ListTile(
                    // leading: CircleAvatar(
                    //   backgroundImage: AssetImage("assets/images/user-default.png"),
                    //   radius: 25,
                    // ),
                      title: Text(controller.discussions[index]["username"].toString(), style: TextStyle(color: ThemeColors.white, fontSize: 16 ,fontWeight: FontWeight.bold),),
                       subtitle: Text(controller.discussions[index]["lastMessage"], style: TextStyle(color: ThemeColors.white, fontSize: 14, overflow: TextOverflow.ellipsis),),
                      trailing: Text(controller.discussions[index]["time"], style: TextStyle(color: ThemeColors.white, fontSize: 13),),
                      onTap: () {
                        pushNamed(routeName: Routes.chat, addToBack: true, arguments: {"roomId":controller.discussions[index]["roomId"], "username":controller.discussions[index]["username"]});
                      },
                  );
              }
            ),
          )
        )
        )
    );

  }

}
