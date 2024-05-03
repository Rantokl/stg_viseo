import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:flutter_svg/svg.dart';
import 'package:sav/models/constant/values/assets.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/rdv/mes_rdv.dto.dart';
import 'package:sav/models/dto/sav/etape_sav.dto.dart';
import 'package:sav/models/dto/vehicle/vehicle.dto.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';

class CustomCard {
  static Widget details(
      {required String number,
      required String model,
      required String specification}) {
    return Container(
      decoration: BoxDecoration(color: ThemeColors.gray),
      width: double.infinity,
      child: Padding(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              number,
              style: TextStyle(
                  color: ThemeColors.dark,
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  decoration: TextDecoration.none),
            ),
            SizedBox(
              height: 10,
            ),
            Text(
              model,
              style: TextStyle(
                  color: ThemeColors.dark,
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  decoration: TextDecoration.none),
            ),
            SizedBox(height: 10),
            Text(
              specification,
              style: TextStyle(
                  color: ThemeColors.dark,
                  fontSize: 14,
                  fontWeight: FontWeight.normal,
                  decoration: TextDecoration.none),
            ),
          ],
        ),
      ),
    );
  }

  static Widget menu(
      {required String iconPath,
      required String libelle,
      required VoidCallback? onPressed}) {
    return ListTile(
      onTap: onPressed,
      leading: Container(
          padding: EdgeInsets.all(8.0),
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(10), color: ThemeColors.gray),
          child: SizedBox(
              width: 20,
              height: 20,
              child: SvgPicture.asset(
                iconPath,
                colorFilter:
                    const ColorFilter.mode(ThemeColors.dark, BlendMode.srcIn),
              ))),
      title: Text(
        libelle,
        style: TextStyle(color: ThemeColors.white),
      ),
    );
  }

  static Widget description({required List text, bool? centerText}) {
    return Padding(
        padding: EdgeInsets.symmetric(horizontal: 20, vertical: 20),
        child: Column(
          children: [
            Padding(
              padding: EdgeInsets.only(bottom: 10),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: text
                    .map((text) => Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            Text(
                              text["text"],
                              style: TextStyle(
                                  height: 1.5,
                                  color: ThemeColors.white,
                                  fontWeight: text["isBold"] == true
                                      ? FontWeight.bold
                                      : FontWeight.normal,
                                  fontSize: text["size"]),
                              textAlign: centerText == true
                                  ? TextAlign.center
                                  : TextAlign.justify,
                            ),
                            SizedBox(
                              height: 10,
                            )
                          ],
                        ))
                    .toList(),
              ),
            ),
            const Divider(
              color: ThemeColors.white,
            ),
          ],
        ));
  }

  static Widget Devis({
    required String title,
    required String resume,
    required String price,
    required List<String> status,
    required String date,
  }) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 10, horizontal: 20),
      child: Card(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12.0),
        ),
        color: Color(0xFF343434),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ListTile(
              title: Row(
                children: [
                  SizedBox(
                    width: 150,
                    child: Text(
                      title,
                      style: const TextStyle(
                          color: Colors.white, fontWeight: FontWeight.bold),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  const Spacer(),
                  Text(
                    price,
                    style: TextStyle(
                        color: Colors.white, fontWeight: FontWeight.bold),
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
              subtitle: Text(
                resume,
                style: const TextStyle(color: Colors.white),
                overflow: TextOverflow.ellipsis,
              ),
            ),
            Padding(
              padding: EdgeInsets.only(right: 16, left: 16, bottom: 10),
              child: Align(
                alignment: Alignment.bottomCenter,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        const Icon(
                          Icons.calendar_today,
                          color: Colors.white,
                        ),
                        const SizedBox(width: 10),
                        Text(
                          date,
                          style: const TextStyle(color: Colors.white),
                        ),
                      ],
                    ),
                    Padding(
                      padding: const EdgeInsets.only(left: 50),
                      child: Row(
                        children: [
                          SvgPicture.asset(status[0]),
                          const SizedBox(width: 10),
                          Text(
                            status[1],
                            style: const TextStyle(color: ThemeColors.white),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }


  static Widget Rdv ({
    required String title,
    required String description,
    required String date,
    required List<String> status,
  }) {
    return Container(
      width: 370,
      height: 125,
      padding: EdgeInsets.symmetric(horizontal: 20.0),
      child: Card(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12.0),
        ),
        color: ThemeColors.black,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ListTile(
              minVerticalPadding: 10.0,
              title: Padding(
                padding: const EdgeInsets.only(bottom: 8.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(color: ThemeColors.white, fontWeight: FontWeight.bold),
                    ),
                    if (status[1] == Strings.statut.waiting)  Icon(Icons.edit, color: Colors.orange)
                  ],
                ),
              ),
              subtitle: Tooltip(
                triggerMode: TooltipTriggerMode.longPress,
                message: description,
                child: Text(
                  description,
                  style: const TextStyle(
                      color: ThemeColors.white,
                      overflow: TextOverflow.ellipsis),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(right: 16, left: 16),
              child: Row(
                children: [
                  Row(
                    children: [
                      const Icon(
                        Icons.calendar_today,
                        color: ThemeColors.white,
                      ),
                      const SizedBox(width: 10),
                      Text(
                        date,
                        style: const TextStyle(color: ThemeColors.white),
                      ),
                    ],
                  ),
                  Padding(
                    padding: const EdgeInsets.only(left: 50),
                    child: Row(
                      children: [
                        SvgPicture.asset(status[0]),
                        const SizedBox(width: 10),
                        Text(
                          status[1],
                          style: const TextStyle(color: ThemeColors.white),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const Spacer(),
          ],
        ),
      ),
    );
  }

  static Widget Vehicle({
    required VehicleDto? vehiculeDto,
    required double textScale,
    required void Function()? onTapPic,
    required void Function()? onTap,  
  }) {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12.0),
      ),
      color: ThemeColors.gray,
      child: Align(
        alignment: Alignment.centerLeft,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            GestureDetector(
              onTap: onTapPic,
              child: AspectRatio(
                aspectRatio: 1.5 / textScale, // Rapport hauteur / largeur fixe
                child: ClipRRect(
                    borderRadius: const BorderRadius.only(
                      topLeft: Radius.circular(12.0),
                      topRight: Radius.circular(12.0),
                    ),
                    child: Container(
                        decoration: BoxDecoration(color: ThemeColors.black),
                        child: (vehiculeDto!.image != null)
                            ? Image.network(
                                vehiculeDto!.image!,
                                fit: BoxFit.cover,
                                errorBuilder: (context, error, stackTrace) {
                                  // Image non chargée
                                  return Image.asset(
                                    Assets.logo,
                                    fit: BoxFit.fitWidth,
                                  );
                                },
                              )
                            : Image.asset(
                                Assets.logo,
                                fit: BoxFit.contain,
                              ))),
              ),
            ),
            GestureDetector(
              onTap: onTap,
              child: ListTile(
                title: Text(
                  vehiculeDto!.number ?? '',
                  // overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                      color: ThemeColors.black,
                      fontWeight: FontWeight.bold),
                ),
                subtitle: Text(
                  vehiculeDto!.model,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(color: ThemeColors.black),
                ),
              ),
            ),
            GestureDetector(
              onTap: onTap,
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: ThemeSpacing.m),
                child: Text(
                  vehiculeDto.specification ?? '',
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(color: ThemeColors.black),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }

  static String _getStatusName(int status) {
    if (status == 1) {
      return "En cours";
    } else if (status == 2) {
      return "Annulé";
    }
    return "Terminé";
  }

  static Widget sav({
    required String title,
    required String type,
    required String date,
    required List<String> status,
    List<EtapesavDto>? listsav,
  }) {
    RxBool isExpanded = false.obs;
    var current = listsav?.firstWhere(
        (element) => element.libelle == "en cours",
        orElse: () => EtapesavDto(etape: "", status_id: 0, libelle: ""));
    var currentEtape =
        current?.etape.isNotEmpty == true ? "  -  ${current!.etape}" : "";
    return Padding(
      padding: EdgeInsets.only(left: 10, right: 10, top: 5),
      child: Card(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12.0),
          ),
          color: Color(0xFF343434),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 10),
            child: Column(
              children: [
                ExpansionTile(
                  title: Text(title + currentEtape,
                      style: const TextStyle(
                          color: Colors.white, fontWeight: FontWeight.bold)),
                  subtitle: Text('Type : $type',
                      style: const TextStyle(color: Colors.white, height: 1.8)),
                  iconColor: ThemeColors.white,
                  trailing: AnimatedSwitcher(
                    duration: Duration(milliseconds: 500),
                    child: Obx(() => isExpanded.value == true
                        ? Icon(
                            Icons.keyboard_arrow_up, // icône vers le haut
                            color: Colors.white,
                          )
                        : Icon(
                            Icons.keyboard_arrow_down, // icône vers le bas
                            color: Colors.white,
                          )),
                  ),
                  onExpansionChanged: (expanded) {
                    isExpanded.value = !isExpanded.value;
                  },
                  children: listsav == null
                      ? []
                      : listsav
                          .map(
                            (sav) => Padding(
                              padding:
                                  const EdgeInsets.symmetric(horizontal: 10),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Divider(
                                    color: Colors.white,
                                  ),
                                  Padding(
                                    padding:
                                        const EdgeInsets.symmetric(vertical: 5),
                                    child: Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      children: [
                                        SizedBox(
                                          width: 200,
                                          child: Row(
                                            children: [
                                              Icon(
                                                  Icons
                                                      .subdirectory_arrow_right_outlined,
                                                  color: Color.fromARGB(
                                                      255, 92, 92, 92)),
                                              const SizedBox(width: 10),
                                              Text(
                                                sav.etape,
                                                style: TextStyle(
                                                    color: Colors.white,
                                                    fontWeight: FontWeight.bold,
                                                    overflow:
                                                        TextOverflow.ellipsis),
                                              ),
                                            ],
                                          ),
                                        ),
                                        Tooltip(
                                          triggerMode: TooltipTriggerMode.tap,
                                          verticalOffset: -18,
                                          margin: EdgeInsets.only(right: 45),
                                          message:
                                              _getStatusName(sav.status_id),
                                          child: SvgPicture.asset(
                                              sav.getStatus(sav.status_id)),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          )
                          .toList(),
                ),
                Align(
                  alignment: Alignment.bottomCenter,
                  child: Padding(
                    padding: const EdgeInsets.only(
                        left: 13, right: 13, bottom: 14, top: 5),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Row(
                          children: [
                            const Icon(
                              Icons.calendar_today,
                              color: Colors.white,
                            ),
                            const SizedBox(width: 10),
                            Text(
                              date,
                              style: const TextStyle(color: Colors.white),
                            ),
                          ],
                        ),
                        Row(
                          children: [
                            SvgPicture.asset(status[0]),
                            const SizedBox(width: 10),
                            Text(
                              status[1],
                              style: const TextStyle(color: Colors.white),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          )),
    );
  }

  static Widget Contact(
      {required String title,
      required String description,
      required List<ContactItem> items,
      Color enteteColor = ThemeColors.blue}) {
    return Container(
      child: Card(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12.0),
        ),
        color: ThemeColors.dark,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(15.0),
              decoration: BoxDecoration(
                color: enteteColor, // Couleur de l'en-tête
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(12.0),
                  topRight: Radius.circular(12.0),
                ),
              ),
              child: Text(
                title,
                style: const TextStyle(
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                  fontSize: 16.0,
                ),
              ),
            ),
            const SizedBox(height: 12.0),
            Padding(
              padding: EdgeInsets.only(left: 16, right: 16, bottom: 16),
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      description,
                      style: TextStyle(color: Colors.white),
                    ),
                    const SizedBox(height: 10),
                    Column(
                      children: items.map((item) {
                        return itemWidget(item.icon, item.text);
                      }).toList(),
                    ),
                  ]),
            )
          ],
        ),
      ),
    );
  }

  static Widget itemWidget(IconData icon, String text) {
    return Column(children: [
      Row(
        children: [
          Icon(
            icon,
            color: Colors.white,
          ),
          const SizedBox(width: 10),
          Expanded(
              child: Text(text,
                  style: TextStyle(color: Colors.white, height: 1.5)))
        ],
      ),
      const SizedBox(height: 5.0),
    ]);
  }

  String getStatus(int status) {
    if (status == 1) {
      return Assets.icons.check;
    } else if (status == 2) {
      return Assets.icons.dots;
    }
    return Assets.icons.minus;
  }

  static Widget notif({
    required String title,
    required String resume,
    String? date,
  }) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 10, horizontal: 20),
      child: Card(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12.0),
        ),
        color: Color(0xFF343434),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ListTile(
              title: Text(title,
                  style: const TextStyle(
                      color: Colors.white, fontWeight: FontWeight.bold),
                  overflow: TextOverflow.ellipsis),
              subtitle: Text(
                resume,
                style: const TextStyle(color: Colors.white),
                overflow: TextOverflow.ellipsis,
              ),
            ),
            Padding(
              padding: EdgeInsets.only(right: 16, left: 16, bottom: 10),
              child: Align(
                alignment: Alignment.bottomCenter,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        const Icon(
                          Icons.calendar_today,
                          color: Colors.white,
                        ),
                        const SizedBox(width: 10),
                        Text(
                          date!,
                          style: const TextStyle(color: Colors.white),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class ContactItem {
  final IconData icon;
  final String text;

  ContactItem({required this.icon, required this.text});
}
