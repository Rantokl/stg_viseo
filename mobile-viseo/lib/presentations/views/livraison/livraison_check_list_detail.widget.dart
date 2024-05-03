
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:sav/presentations/views/widgets/checkBox/checkBox.widget.dart';

class LivraisonCheckListDetailWidget extends StatelessWidget {
  final int item_id;
  final int id;
  final String libelle;
  final bool isCheck;
  final Function changeCheckItem;
  const LivraisonCheckListDetailWidget({Key? key,
    required this.item_id,
    required this.id,
    required this.libelle,
    required this.isCheck, 
    required this.changeCheckItem, 
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return GestureDetector(
      onTap: () {
        changeCheckItem(item_id, id);
      },
      child: Row(
        children: [
          CheckBoxWidget(item_id: item_id, id: id,isCheck: isCheck, onChange: changeCheckItem),
          Text(
            libelle,
            style: TextStyle(color: Colors.white),
          )
        ],
      ),
    );
  }
  
}