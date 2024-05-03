import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/models/dto/devis/devis.dto.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/devis/devis_pdf.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';
import 'package:syncfusion_flutter_pdfviewer/pdfviewer.dart';
import 'dart:io';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as path;
import 'package:permission_handler/permission_handler.dart';

import '../../../models/constant/values/assets.dart';

class DevisPdfView extends BaseStatelessView<DevisPdfController> {
   DevisPdfView({
    Key? key,
    required this.devis,
    required this.fromNotif
  }) : super(key: key, controller: Get.put(DevisPdfController()));
   
   final DevisDto devis;
   final bool fromNotif ;

   late double _screenWidth;
   late double _screenHeight;

   var dio = Dio();
   final GlobalKey<SfPdfViewerState> _pdfViewerKey = GlobalKey();


   void validation(int id, int validation, BuildContext context) {
    controller.validation(
      id: id, 
      validation: validation,
      success: (isSucces) {
       if (isSucces) {
         if(validation == 2 ) {
          _showConfirmationModal(devis.numero_devis!, context);
         } else {
          Get.back();
         }
       }
       },
       failure: (response){
         if (response.statusCode == Strings.common.expiredTokenCode) {
           showTokenExpiredModal();
         }
         else {
           showErrorDialog(
               title: "Erreur", message: controller.messageResponse);
         }
      }
      );
   }

   void _showConfirmationModal(String numero_devis, BuildContext context) {
    Get.dialog(
      CustomModal.simpleModal(
          icon: SvgPicture.asset("assets/check.svg", height: 20,),
          title: "Le devis n°${numero_devis} a été validé",
          description: "Nous prenons en compte votre demande",
          onPressed: () {
            Navigator.of(context).pop();
            Get.back();
          }
          ),
      barrierDismissible: false,
    );
  }

  void download() async {
      
      Directory? downloadDirectory = Directory("/storage/emulated/0/Download");

      // Define the file name for the downloaded PDF
      String fileName = "${devis.numero_devis}_devis.pdf";
      String filePath = path.join(downloadDirectory.path, fileName);

      // Load the PDF asset
      // Download the PDF file
      dynamic response = await dio.get(devis.pdf!, options: Options(responseType: ResponseType.bytes));
      List<int> bytes = response.data;

      // Write the PDF data to the file in the download directory
      File file = File(filePath);
      await file.writeAsBytes(bytes);

      showToast(title: "Téléchargement", message: "Fichier téléchargé dans : ${file.path}");
  
  }

  
  @override
Widget build(BuildContext context) {
  _screenWidth = MediaQuery.of(context).size.width;
  _screenHeight = MediaQuery.of(context).size.height;
  print("========= ${devis.pdf}");
  return baseScaffoldView(
    appBarController: AppBarController(
      title: fromNotif == false ? controller.vehicleSelected?.number : controller.vehicleNotif?.number,
    ),
    withHeader: true,
    fromNotif: fromNotif,
    body: Obx(() => controller.isLoading
        ? Container()
        : Expanded(
          child: SingleChildScrollView( // Wrap in SingleChildScrollView
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Padding(
                      padding: EdgeInsets.symmetric(vertical: 16),
                      child: SizedBox(
                        width: _screenWidth,
                        height: _screenHeight * 55 / 100, // Set a fixed height for the viewer
                        child: SfPdfViewer.network(
                          
                          devis.pdf!,
                          pageSpacing: 40,
                          key: _pdfViewerKey,
                        ),
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.symmetric(horizontal: 16),
                      child: Column(
                        children: [
                          if (devis.status_devis == Strings.statut.waiting)
                            Padding(
                              padding: const EdgeInsets.only(bottom: 10),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  CustomeButton.elevated(
                                      // horizontal: _screenWidth / 2.25,
                                      vertical: _screenHeight / 14.8,
                                      fontSize: ThemeSpacing.ml,
                                      onPressed: () =>
                                          validation(devis.devis_id, 1, context),
                                      buttonTitle: Strings.common.dismiss,
                                      color: ThemeColors.red,
                                      isRow: true
                                  ),
                                  HorizontalSpace.m,
                                  CustomeButton.elevated(
                                      horizontal: _screenWidth / 2.25,
                                      vertical: _screenHeight / 14.8,
                                      fontSize: ThemeSpacing.ml,
                                      onPressed: () =>
                                          validation(devis.devis_id, 2, context),
                                      buttonTitle: Strings.common.accept,
                                      color: ThemeColors.green,
                                      isRow: true
                                  ),  
                                ],
                              ),
                            ),
                          CustomeButton.elevated(
                              horizontal: _screenWidth,
                              fontSize: ThemeSpacing.ml,
                              onPressed: () => pushNamed(routeName: Routes.devisCommentaire, arguments: fromNotif == false ? {"devis": devis, "fromNotif": false} : {"devis": devis, "fromNotif": true}),
                              buttonTitle: Strings.devis.commentaire,
                              color: ThemeColors.gray
                          ),
                          TextButton(
                            style: TextButton.styleFrom(
                              textStyle: const TextStyle(fontSize: 20),
                            ),
                            onPressed: () => download(),
                            child: Text(Strings.devis.downloadPdf),
                          ),
                        ],
                      ),
                    )

                  ],
                ),
              ),
        ),
          ),
  );
}
}