class Urls {
  static const String base = "http://41.188.18.12:32310/api/v1"; // VISEO

  // User
  static _User user = _User();

  // Vehicle
  static _Vehicle vehicle = _Vehicle();

  // Devis
  static _Devis devis = _Devis();

  // Rendez-vous
  static _Rdv rdv = _Rdv();

  // Panique
  static _Panic panic = _Panic();

  // Réclamation
  static _Reclamation reclamation = _Reclamation();

  // Garantie
  static _Garantie garantie = _Garantie();

  // Contrat
  static _Contrat contrat = _Contrat();

  //sav
  static _Sav sav = _Sav();

  //notification
  static _Notification notification= _Notification();

  //notification
  static _Evaluation evaluation= _Evaluation();

  //link
  static _Link link= _Link();

  // Contact
  static _Contact contact = _Contact();

  //chat
  static _Chat chat = _Chat();

  // mdpOublier
  static _MdpOublier mdpOublier = _MdpOublier();

  //livraison
  static _Livraison livraison = _Livraison();

  static _UploadVehicle uploadVehicle = _UploadVehicle();
}

class _User {
  String get login => "/login/";
  String get profile => "/profile";
  String get logout => "/logout";
  String get refreshToken => "/refresh_token/";
  String get check_lifetime_token => "/check_lifetime_token/";
}

class _Vehicle {
  String get list => "/vehicles";
  String get search => "/vehicle_number";
  String get detail => "/vehicle_details";
}

class _Devis {
  String get typeDevis => "/type_devis";
  String get demandeDevis => "/demande_devis";
  String get listDevis => "/liste_devis";
  String get validationDevis => "/validation_devis";
  String get postCommentaire => "/commentaire_devis";
}

class _Rdv {
  String get dateRdv => "/date_rendez_vous/";
  String get typeRdv => "/type_rendez_vous/";
  String get priseRdv => "/rendez_vous";
  String get updateRdv => "/update_rendez_vous";
  String get mesRdv => "/mes_rendez_vous";
  String get heurRdv => "/heure_rendez_vous";
  String get dateActuelle => "/date_actuelle";
  String get heurePrise => "/date_heure_prise_rendez_vous";
}

class _Panic {
  String get menuPanic => "/panique";
  String get sendPanic => "/panique_alert";
}
class _Reclamation {
  String get typeReclamation => "/type_reclamations/";
  String get reclamationClient => "/reclamation";
}

class _Garantie {
  String get carnetGarantie => "/check_carnet";
}

class _Contrat {
  String get contratEntretien => "/check_contrat";
}

class _Sav{
  String get sav => "/check_suivi_sav";
}

class _Notification {
  String get fbm => "/fbm_token";
  String get notif => "/check_notification";
  String get read => "/read_notification";
}

class _Evaluation {
  String get evaluation => "/check_question_evaluation";
  String get prestation => "/evaluation_prestation";
}

class _Link {
  String get link => "/generate_link";
}

class _Contact {
  String get contactList => "/check_contact";
}

class _Chat {
  String get checkRoom => "/check_room";
  String get checkRoomAdmin => "/check_room_admin";
  String get updateRoomMessage => "/update_room_message";
}

class _MdpOublier {
  String get mdpOublier => "/reset_password";
}

class _Livraison {
  String get checkListLivraisonByVehicle => "/checklist_livraison";
  String get checkListLivraison => "/checklist_livraisons";
  String get checklistItems => "/checklist_items";
}

class _UploadVehicle {
  String get upload => "/upload_image_vehicle";
}