import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:get/get.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sav/common/theme/theme.utils.dart';
import 'package:sav/models/constant/routes.dart';
import 'package:sav/models/constant/values/strings.dart';
import 'package:sav/presentations/controllers/app_bar/app_bar.controller.dart';
import 'package:sav/presentations/controllers/contrat/contrat_entretien.controller.dart';
import 'package:sav/presentations/views/base_stateless.view.dart';
import 'package:sav/presentations/views/widgets/button/custom_button.widget.dart';
import 'package:sav/presentations/views/widgets/modal/modal.widget.dart';
import 'package:syncfusion_flutter_pdfviewer/pdfviewer.dart';
import 'dart:io';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as path;
import 'package:permission_handler/permission_handler.dart';

class ContratEntretienView extends BaseStatelessView<ContratEntretienController> {
   ContratEntretienView({
    Key? key,
  }) : super(key: key, controller: Get.put(ContratEntretienController())){
     WidgetsBinding.instance!.addPostFrameCallback((_) {
       controller.getContratEntretien(
           success: (success) {

           },
           failure: (response) {
             if (response.statusCode == Strings.common.expiredTokenCode){
               showTokenExpiredModal();
             }
           }
       );
     });
   }
  

   late double _screenWidth;
   late double _screenHeight;

   var dio = Dio();
   final GlobalKey<SfPdfViewerState> _pdfViewerKey = GlobalKey();


  void download() async {

      Directory? downloadDirectory = Directory("/storage/emulated/0/Download");

      // Define the file name for the downloaded PDF
      String fileName = "${controller.vehicleSelected?.number}_contrat_entretien.pdf";
      String filePath = path.join(downloadDirectory.path, fileName);

      // Load the PDF asset
      // Download the PDF file
      dynamic response = await dio.get(controller.contratEntretien.value!.data.first.pdf, options: Options(responseType: ResponseType.bytes));
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

    return baseScaffoldView(
      appBarController: AppBarController(
        title: Strings.contrat.contratEntretienTitle,
      ),
      withHeader: true,
      body: Obx(() => controller.isLoading
          ? Container()
          : Expanded(
            child: controller.contratEntretien.value == null ? Expanded(
                    child: Container(
                      alignment: Alignment.center, // Center the text both vertically and horizontally
                      child: Text(
                        Strings.contrat.noPdf,
                        style: TextStyle(color: ThemeColors.white),
                      ),
                    ),
                  ) : SingleChildScrollView( // Wrap in SingleChildScrollView
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Padding(
                          padding: EdgeInsets.symmetric(vertical: 16),
                          child: SizedBox(
                            width: _screenWidth,
                            height: _screenHeight * 60 / 100, // Set a fixed height for the viewer
                            child: SfPdfViewer.network(
                              controller.contratEntretien.value!.data.first.pdf,
                              pageSpacing: 40,
                              key: _pdfViewerKey,
                            ),
                          ),
                        ),
                        Padding(
                          padding: EdgeInsets.symmetric(horizontal: 16),
                          child: Column(
                            children: [
                              TextButton(
                                style: TextButton.styleFrom(
                                  textStyle: const TextStyle(fontSize: 20),
                                ),
                                onPressed: () => download(),
                                child: Text(Strings.contrat.downloadPdf),
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