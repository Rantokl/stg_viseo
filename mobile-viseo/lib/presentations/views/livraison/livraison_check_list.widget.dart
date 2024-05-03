// ignore_for_file: public_member_api_docs, sort_constructors_first

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:sav/models/dto/livraison/check_list_livraison/check_list_livraison.dto.dart';
import 'package:sav/presentations/views/livraison/livraison_check_list_detail.widget.dart';

class LivraisonCheckListWidget extends StatelessWidget {
  final CheckListLivraisonDto checkListLivraison;
  final Function changeCheckItem;
  const LivraisonCheckListWidget({
    Key? key,
    required this.checkListLivraison,
    required this.changeCheckItem,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    // return Text('text');
    List<String?> categories = <String>[];
    return Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // affiche title si les details du checkliste n' a pas de categorie -- sin non : affiche rien
            getTitleListCheck()??
            SizedBox(height: 8),
            Column(
              children: checkListLivraison.details.map(
                (item) {
                  if(item.categorie != null && !categories.contains(item.categorie)){
                    categories.add(item.categorie);
                    return Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                           SizedBox(height: 20),
                          Text('${checkListLivraison.label} - ${item.categorie}',
                           style: TextStyle(
                            color: Colors.white,
                            fontSize: 15
                            ),
                          ),
                          LivraisonCheckListDetailWidget(
                          item_id : checkListLivraison.items_id,
                          id: item.id,
                          libelle : item.libelle, 
                          isCheck: item.isChecked,
                          changeCheckItem: changeCheckItem,
                          )
                        ],
                      );
                  }else{
                    return LivraisonCheckListDetailWidget(
                      item_id : checkListLivraison.items_id,
                      id: item.id,
                      libelle : item.libelle, 
                      isCheck: item.isChecked,
                      changeCheckItem: changeCheckItem,
                    );
                  }
                  }
              ).toList()
            ),

          ],
    );
  }

  // verification si le checkList ont une categorie
  Widget? getTitleListCheck() {
    bool haveSubgroup = false;
    checkListLivraison.details.forEach(
      (item){
        if(item.categorie != null){
          haveSubgroup = true;
        }
      }
    );

    if(!haveSubgroup){
      return Column(
        children: [
          SizedBox(height: 20),
          Text(
            checkListLivraison.label,
            style: TextStyle(
              color: Colors.white,
              fontSize: 15
            )
          ),
        ],
      );
    }
    return null;
  }

}
