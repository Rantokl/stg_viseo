import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/presentations/views/camera/camera.view.dart';
import 'package:sav/presentations/views/camera/view_img.view.dart';
import 'package:sav/presentations/views/evaluation/evaluation.view.dart';
import 'package:sav/presentations/views/livraison/livraison_message.view.dart';
import 'package:sav/presentations/views/mdpOublier/mdp_oublier.view.dart';
import 'package:sav/presentations/views/contact/contact.view.dart';
import 'package:sav/presentations/views/chat/chat.view.dart';
import 'package:sav/presentations/views/chat/chat_admin.view.dart';
import 'package:sav/presentations/views/contrat/contrat_entretien.view.dart';
import 'package:sav/presentations/views/devis/devis_commentaire.view.dart';
import 'package:sav/presentations/views/devis/devis_pdf.view.dart';
import 'package:sav/presentations/views/devis/list_devis.view.dart';
import 'package:sav/presentations/views/garantie/carnet_garantie.view.dart';
import 'package:sav/presentations/views/livraison/livraison_check.view.dart';
import 'package:sav/presentations/views/auth/login.view.dart';
import 'package:sav/presentations/views/main.view.dart';
import 'package:sav/presentations/views/devis/demande_devis.view.dart';
import 'package:sav/presentations/views/notification/notification.view.dart';
import 'package:sav/presentations/views/rdv/mes_rdv.view.dart';
import 'package:sav/presentations/views/sav/sav.view.dart';
import 'package:sav/presentations/views/reclamation/reclamation_client.view.dart';
import 'package:sav/presentations/views/splash.view.dart';
import 'package:sav/presentations/views/vehicle/vehicle_detail.view.dart';
import 'package:sav/presentations/views/rdv/prise_rdv.view.dart';

class Routes {
  static const String splash = "/";
  static const String login = "/login";
  static const String mdpOublier = "/mdpOublier";
  static const String main = "/main";
  static const String vehicle = "/vehicle";
  static const String vehicleDetail= "/detail";
  static const String vehiclePriseRdv= "/vehiclePriseRdv";
  static const String vehicleDemandeDevis= "/vehicleDemandeDevis";
  static const String mesRdv= "/mesRdv";
  static const String livraisonCheck = "/livraison_check";
  static const String livraisonMessage = "/livraison_message";
  static const String listDevis = "/listDevis";
  static const String devisPdf = "/devisPdf";
  static const String devisCommentaire = "/devisCommentaire";
  static const String suiviSav = "/suiviSav";
  static const String reclamationClient = "/reclamationClient";
  static const String carnetGarantie = "/carnetGarantie";
  static const String contratEntretien = "/contratEntretien";
  static const String notification= "/notification";
  static const String contact = "/contact";
  static const String evaluation= "/evaluation";

  static const String chat = "/chat";
  static const String chatAdmin = "/chatAdmin";

  static const String camera = "/camera";

  static const String image = "/image";

  static List<GetPage> get pages => [
    GetPage(name: splash,page: () => SplashView()),
    GetPage(name: login, page: () => LoginView()),
    GetPage(name: mdpOublier, page: () => MdpOublierView()),
    GetPage(name: main, page: () => MainView()),
    GetPage(
          name: vehicleDetail,
          page: () => VehicleDetailView(),
        ),
    GetPage(
      name: vehiclePriseRdv,
      page: () => PriseRdvView(),
    ),
    GetPage(
      name: vehicleDemandeDevis,
      page: () => DemandeDevisView(),
    ),
    GetPage(
      name: mesRdv,
      page: () => MesRdvView(),
    ),
    GetPage(
      name: livraisonCheck,
      page: () => LivraisonCheckView(),
    ),
    // GetPage(
    //   name : livraisonMessage,
    //   page: () => LivraisonMessageView(),
    // ),
    GetPage(
      name: listDevis,
      page: () => ListDevisView(),
    ),
    GetPage(
      name: devisPdf,
      page: () => DevisPdfView(devis: Get.arguments["devis"], fromNotif: Get.arguments["fromNotif"],),
    ),
    GetPage(
      name: devisCommentaire,
      page: () => DevisCommentaireView(devis: Get.arguments["devis"], fromNotif: Get.arguments["fromNotif"]),
    ),
    GetPage(
      name: suiviSav,
      page: () => SavView(),
    ),
    GetPage(
      name: reclamationClient,
      page: () => ReclamationClientView(),
    ),
    GetPage(
      name: carnetGarantie,
      page: () => CarnetGarantieView(),
    ),
    GetPage(
      name: contratEntretien,
      page: () => ContratEntretienView(),
    ),
    GetPage(
      name: notification,
      page: () => NotificationView(),
    ),
    GetPage(
      name: contact,
      page: () => ContactView(),
    ),
    GetPage(
      name: chat,
      page: () => ChatView(roomId: Get.arguments["roomId"], username: Get.arguments["username"]),
    ),
    GetPage(
      name: chatAdmin,
      page: () => ChatAdminView(),
    ),
    GetPage(
      name: evaluation,
      page: () => EvaluationView(),
    ),
    GetPage(
      name: camera,
      page: () => CameraView(),
    ),
    GetPage(
      name: image,
      page: () => ViewImgView(img: Get.arguments["img"],),
    ),
  ];
}