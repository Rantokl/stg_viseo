class Strings {
  static final _Common common = _Common();

  //Login
  static final _Login login = _Login();

  //Login
  static final _MdpOublier mdpOublier = _MdpOublier();

  // Devis
  static final _Devis devis = _Devis();

  // Rdv
  static final _Rdv rdv = _Rdv();

  // Statut
  static final _Statut statut = _Statut();

  // Menu
  static final _Menu menu = _Menu();

  // Vehicle
  static final _Vehicle vehicle = _Vehicle();

  // sav
  static final _sav sav = _sav();

  // Reclamation
  static final _Reclamation reclamation = _Reclamation();

  // Garantie
  static final _Garantie garantie = _Garantie();

  // Contrat
  static final _Contrat contrat = _Contrat();

  // Notification
  static final _notification notification= _notification();

  // Contact
  static final _Contact contact = _Contact();

  // Chat
  static final _Chat chat = _Chat();

  // evaluation
  static final _evaluation evaluation  = _evaluation();

  //livraison 
  static final _Livraison livraison = _Livraison();
}

class _Common {
  String get appName => "SAV";
  String get pleaseWait => "Merci de patienter...";
  String get notYet => "Cette opération n'est pas encore implémentée";
  String get fieldRequired => "Ce champ est obligatoire";
  String get passwordRequired => "Le mot de passe est obligatoire";
  String get mailNotValid => "L'email n'est pas valide";
  String get tokenExpiredDescription => "Votre session est expirée, veuillez vous reconnecter";

  String get validate => "Valider";
  String get accept => "Accepter";
  String get dismiss => "Rejeter";
  String get close => "Fermer";
  String get confirm => "Confirmer";
  String get send => "Envoyer";
  String get sended => "Envoyé";
  String get error => "Erreur";
  String get tokenExpired => "Session expirée";

  // Token expiré status Code
  int get expiredTokenCode => 410;
}

class _Login {
  String get title => "Connexion";
  String get email => "Email";
  String get username => "Nom d'utilisateur";
  String get password => "Mot de passe";
  String get submit => "Se connecter";
  String get forgottenPassword => "Mot de passe oublié ?";
}

class _MdpOublier {
  String get envoyer => "Envoyer";
  String get instruction => "Veuillez entrer votre adresse e-mail. Nous vous enverrons un e-mail de confirmation";
  String get titre => "Confirmation";
  String get description => "Votre demande a été envoyée avec succès";
  String get error => "Erreur";
}

class _Statut {
  String get waiting => "Attente";
  String get validated => "Validé";
  String get rejected => "Rejeté";

}

class _Livraison {
  String get title => "Checklist livraison";
  String get reserve => "Valider avec reserve";
  String get indication => "Merci de nous fournir en détails vos réserves pour le véhicule sélectionné";
  String get required => "Veuillez remplir les champs ci-dessous";
  String get yourMessage => "Votre message";
  String get sended =>"Envoyé";
  String get notificationRejected => "Checklist livraison rejeté";
  String get notivicationValidated => "Checklist livraison validé avec succès";
  String get livraisonDejaFait => "La validation de la checklist de livraison est déjà faite";
  String get checklistReject => "La checklist de livraison a été rejetée";
  String get messageConfirmation => "Une fois que vous avez validé la checklist, il n'est plus possible d'apporter des modifications";
  String get messageConfirmationWithReserve => "Vous pourriez apporter des modifications plus tard. \n\n Voulez-vous enregistrer la checklist ?";
}

class _Devis {
  String get devisList => "Liste des devis";

  // Demande de devis
  String get demandeTitle => "Demande de devis";
  String get typeDevis => "Type de devis";
  String get demandePlaceholder => "Votre besoin";
  String get demandeIndication => "Le devis sera envoyé pour étude pour ce véhicule précis";
  String get demandeRequired => "Veuillez remplir les champs ci-dessous et nous reviendrons vers vous et vous notifierons";
  String get notificationTitle => "Nous avons pris en compte votre demande";
  String get notificationDescription => "Votre devis sera disponible dans les meilleurs délais";
  String get sendDemande => "Envoyer la demande";
  String get listDemande => "Liste des demandes";

  // Commentaire
  String get commentaire => "Commentaire";
  String get commentaireTitle => "Commentaire sur le devis";
  String get commentaireRequired => "Veuillez remplir les champs ci-dessous";
  String get commentaireNotification => "Votre commentaire a été envoyé";
  String get commentairePlaceholder => "Votre message";

  // PDF
  String get downloadPdf => "Télécharger le pdf";
}

class _Rdv {
  // Prise de rdv
  String get demandeTitle => "Prise de rdv";
  String get modificationTitle => "Modifier un rdv";
  String get notificationTitle => "Nous avons pris en compte votre demande de RDV";
  String get notificationDescription => "Pour la date du \n";
  String get typeRdv => "Type de rendez-vous";
  String get dateRdv => "Date";
  String get heureRdv => "Heure";
  String get yourMessage => "Votre message";
  String get confirmRdv => "Confirmer mon rendez-vous";
  String get updateRdv => "Modifier mon rendez-vous";
  String get demandeIndication => "Nombre de rendez-vous disponible ce jour : ";
  String get demandeRequired => "Veuillez remplir les champs ci-dessous";
  String get aucuneDateRdv => "Aucune date de rendez-vous disponible";
  String get noMesRdv => "Vous n'avez aucun rdv pour l'instant";
  String get helpText => "Choisir l'heure de RDV [6h à 18h] (les minutes seront toujours 00)";
  String get hourIndicator => "Veuillez choisir une heure de rendez-vous entre 6h et 18h";
  
  String get typeRdvVide => "Veuillez choisir un type de rendez-vous";
  String get dateVide => "Veuillez choisir une date de rendez-vous";
  String get heureVide => "Veuillez choisir une heure de rendez-vous";
  String get heureIndisponible => "Il n'y a pas d'heure disponible pour la date : ";
  String get dateEtTypeVide => "Veuillez choisir un type et une date de rendez-vous";
  // Mes rdv
  String get mesRdvTitle => "Mes rendez-vous";
}

class _Menu {
  // Navigation
  String get panic => "Panique";
  String get vehicles => "Véhicules";
  String get profil => "Profil";
  String get chat => "Chat";

  // Profil
  String get vehicleList => "Liste de mes véhicules";
  String get mesRdv => "Mes rendez-vous";
  String get mesContacts => "Nos contacts";
  String get mesNotifications => "Mes notifications";
  String get facebook => "Suivez-nous sur Facebook";
  String get changePassword => "Modifier mon mot de passe";
  String get avis => "Votre avis nous intéresse";
  String get deconnexion => "Déconnexion";

  // Panic
  String get alertTitle => "Vous êtes sur le point de nous envoyer une alerte pour un souci urgent !";
  String get alertDescri => "Nous reviendrons vers vous afin de vous contacter et de vous envoyer un de nos collaborateurs afin d’intervenir sur le problème alerté";
  String get confirmationPanic => "Vous venez de nous envoyer une alerte";
}

class _Vehicle {
  String get ficheVehicle => "Fiche véhicule";
}

class _sav{
  String get sav => "Parcours sav";
}
class _Reclamation {
  String get reclamationTitle => "Réclamation";
  String get reclamationIndication => "Merci de nous fournir en détails vos soucis pour le véhicule selectionné";
  String get reclamationRequired => "Veuillez remplir les champs ci-dessous";
  String get typeReclamation => "Type de réclamation";
  String get reclamationPlaceholder => "Votre message";
  String get notificationTitle => "Votre réclamation a été prise en compte";
}



class _Garantie {
  String get carnetGarantieTitle => "Carnet de garantie";
  // PDF
  String get downloadPdf => "Télécharger le pdf";
  String get noPdf => "Aucun pdf carnet de garantie pour ce véhicule";
}

class _Contrat {
  String get contratEntretienTitle => "Contrat d'entretien";
  // PDF
  String get downloadPdf => "Télécharger le pdf";
  String get noPdf => "Aucun pdf contrat d'entretien pour ce véhicule";
}

class _notification {
  String get notification => "Notifications";
  String get notifDevis => "Devis";
  String get notifChat => "Chat";
  String get notifRdv => "Rendez-vous";
  
}

class _Contact {
  String get title => "Nos contacts";
  String get noData => "Aucun contact trouvé";
  String get contactTitle => "Adresse concernée";
}

class _Chat {
  String get title => "Chat";
  String get adminTitle => "Liste de discussions";
}

class _evaluation {
  String get error => "Erreur";
  String get title => "Evaluation";
  String get question => "Comment trouvez vous l'application ?";
  String get note => "Repondez aux questions";
  String get comment => "Laissez un commentaire si vous en avez";
  String get addComment => "Ecrivez votre commentaire";
  String get next => "Suivant";
  String get send => "Envoyer";
  String get modalTitle => "Nous vous remercions d'avoir pris le temps de nous répondre";
  String get modalDescription => "Nous essayons d'améliorer nos services afin de répondre à vos besoins. Merci !";

}