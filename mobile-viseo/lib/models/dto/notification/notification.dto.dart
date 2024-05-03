import 'package:sav/models/dto/base.dto.dart';
import 'package:json_annotation/json_annotation.dart';
import 'package:sav/models/dto/devis/devis.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';

part 'notification.dto.g.dart';

@JsonSerializable()
class NotificationDto extends BaseDto {
  int notif_id;
  List<VehicleDto> vehicle;
  List<DevisDto> details;
  bool isRead;
  String type;
  String titre;
  String alerte_message;
  String date_notification;


  NotificationDto({required this.notif_id, required this.vehicle,required this.details, required this.isRead, required this.type, required this.titre, required this.alerte_message, required this.date_notification});

  factory NotificationDto.fromJson(dynamic json) {
    return _$NotificationDtoFromJson(json);
  }

  @override
  bind(serializable) {
    this.notif_id = serializable.notif_id;
    this.vehicle = serializable.vehicle;
    this.details = serializable.details;
    this.isRead = serializable.isRead;
    this.type = serializable.type;
    this.titre = serializable.titre;
    this.alerte_message = serializable.alerte_message;
    this.date_notification = serializable.date_notification;
  }

  @override
  NotificationDto copy() => NotificationDto(notif_id: this.notif_id, vehicle: this.vehicle, details: this.details, isRead: this.isRead, titre: this.titre, type: this.type, alerte_message: this.alerte_message, date_notification: this.date_notification)..bind(this);

  @override
  Map<String, dynamic> toJsonLocal() => _$NotificationDtoToJson(this);

}