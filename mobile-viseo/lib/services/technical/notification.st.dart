import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:get/get.dart';
import 'package:sav/presentations/views/notification/notification.view.dart';
import 'package:sav/services/applying/local/preference.sa.dart';
import 'package:flutter/material.dart';



class NotificationST {
  FirebaseMessaging _fcm = FirebaseMessaging.instance;
  FlutterLocalNotificationsPlugin _flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();
  PreferenceSA pref = PreferenceSA.instance;

  Future initialize() async {

    WidgetsFlutterBinding.ensureInitialized();
    await Firebase.initializeApp();

    NotificationSettings settings = await _fcm.requestPermission(
      alert: true,
      announcement: false,
      badge: true,
      carPlay: false,
      criticalAlert: false,
      provisional: false,
      sound: true,
    );
    
    if(settings.authorizationStatus == AuthorizationStatus.authorized) {
      FirebaseMessaging.onMessage.listen((RemoteMessage message) {
          print("onMessage event");
          print('Got a message whilst in the foreground!');
          print('Message data: ${message.data}');

          if (message.notification != null) {
            print('Message also contained a notification: ${message.notification}');
            if (message.notification!.title != null) {
              print('Notification title: ${message.notification!.title}');
            }
            if (message.notification!.body != null) {
              print('Notification body: ${message.notification!.body}');
            }
            if (message.notification!.title != null && message.notification!.body != null) {
              _showLocalNotification(
                message.notification!.title!,
                message.notification!.body!,
              );
            }
          }
      });

      FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message){
        print("onMessageOpenedApp event");
        Get.to(NotificationView());
      });

      Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
        // Gérer les messages en arrière-plan ici.
        _showLocalNotification(
          message.notification!.title!,
          message.notification!.body!,
        );
      }

      FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);
    }
  }


  void _showLocalNotification(String title, String body) async {

    var androiInit = const AndroidInitializationSettings('@mipmap/ic_notification');  
    var initSetting = InitializationSettings(android: androiInit);
    _flutterLocalNotificationsPlugin.initialize(initSetting);

    const AndroidNotificationDetails androidPlatformChannelSpecifics =
        AndroidNotificationDetails(
      'viseo_hight_notification',
      'Viseo Notifications',
      channelDescription: 'This is important notifications from viseo.',
      importance: Importance.max,
      priority: Priority.high,
      playSound: true,
      showWhen: false,
    );

    const NotificationDetails platformChannelSpecifics =
        NotificationDetails(android: androidPlatformChannelSpecifics);

    pref.notifLenght.value += 1;
    print('notif lenght ======== ${pref.notifLenght}');

    await _flutterLocalNotificationsPlugin.show(
      0,
      title,
      body,
      platformChannelSpecifics,
    );
  }

}
