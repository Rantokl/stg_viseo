import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/chat/chat.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;

class ChatView extends BaseStatelessView<ChatController> {
  ChatView({
    required this.roomId,
    required this.username,
    Key? key
  }) : super(key: key, controller: Get.put(ChatController(roomId: roomId, username: username)));

  final int roomId;
  final String username;

   void logout() async {
    await controller.logout(success: (isSuccess) {
      pushNamed(routeName: Routes.login, addToBack: false);
    });
  }

  @override
  Widget build(BuildContext context) {
    return baseScaffoldView(
        appBarController: AppBarController(
            title: Strings.chat.title,
            logout: logout
        ),
        body: Obx(() => controller.isLoading
            ? Container()
            : Expanded(
              child: Padding(
                padding: const EdgeInsets.all(5.0),
                child: Chat(
                    l10n: const ChatL10nEn(
                      emptyChatPlaceholder: "Aucun message",
                      inputPlaceholder: "Votre message",
                    ),
                    theme: const DefaultChatTheme(
                      backgroundColor: ThemeColors.blackTheme,
                      inputBackgroundColor: ThemeColors.gray,
                      inputTextColor: ThemeColors.dark,
                      userAvatarNameColors: [Colors.deepPurpleAccent],
                      userNameTextStyle: TextStyle(color: Colors.deepPurpleAccent, fontWeight: FontWeight.bold),
                    ),
                  customBottomWidget: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Container(
                      decoration: BoxDecoration(
                        color: ThemeColors.gray, // Couleur de fond de la zone de saisie
                        borderRadius: BorderRadius.circular(20.0), // Ajoutez le border radius souhaité
                      ),
                      padding: const EdgeInsets.all(8.0), // Espacement interne
                      child: Row(
                        children: [
                          Expanded(
                            child: TextField(
                              controller: controller.messageController,
                              decoration: InputDecoration(
                                hintText: "Votre message",
                                border: InputBorder.none,
                              ),
                            ),
                          ),
                          IconButton(
                            icon: Icon(Icons.send),color: ThemeColors.dark,
                            onPressed: () {
                              final messageContent = types.PartialText(
                                text: controller.messageController.text,
                              );
                              controller.handleSendPressed(messageContent);

                              controller.messageController.clear();
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                    messages: controller.messages,
                    // onAttachmentPressed: controller.handleAttachmentPressed,
                    onMessageTap: controller.handleMessageTap,
                    onPreviewDataFetched: controller.handlePreviewDataFetched,
                    onSendPressed: controller.handleSendPressed,
                    user: controller.user,
                    // onEndReached: controller.handleEndReached,
                    // showUserAvatars: true,
                    showUserNames: true,
                  dateLocale: "fr_FR",
                ),
              ),
            )
        )
    );

  }

}
