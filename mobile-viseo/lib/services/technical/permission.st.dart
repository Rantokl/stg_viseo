import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:sav/common/utils/app.utils.dart';

class PermissionST {

  static checkPermissions({
    VoidCallback? onGranted,
    CompletionClosure<String>? onRejected,
    CompletionClosure<String>? onPermanentlyDenied,
    required dynamic permissions
  }) {
    var permissionsUseful = _permissionsUseful(permissions);
    if (permissionsUseful != null) {
      _requestPermission(permissionsUseful).then((status) async {
        var granted = false;
        var message = "permissionRequired";
        if(status.isGranted){
          granted = true;
        } else if (status.isPermanentlyDenied) {
          message = "permissionRestricted";
          openAppSettings();
        }

        if (granted) {
          onGranted?.call();
        } else {
          if (status != PermissionStatus.permanentlyDenied) {
            onRejected?.call(message);
          }
        }
      });
    } else {
      onGranted?.call();
    }
  }

  static Future<dynamic> request(permissions) async {
    if (permissions is Permission) {
      return await permissions.request();
    }

    if (permissions is List<Permission>) {
      return await permissions.request();
    }
    return PermissionStatus.denied;
  }

  static bool _permissionUseful(Permission permission) {
    if (GetPlatform.isAndroid) {
      return permission != Permission.unknown;
    } else if (GetPlatform.isIOS) {
      return permission != Permission.unknown;
    }
    return true;
  }

  static dynamic _permissionsUseful(permissions) {
    if (permissions is Permission) {
      if (_permissionUseful(permissions)) {
        return permissions;
      }
    }

    if (permissions is List<Permission>) {
      var results = <Permission>[];
      permissions.forEach((permission) {
        if (_permissionUseful(permission)) {
          results.add(permission);
        }
      });
      if (results.isEmpty) {
        return null;
      }
      return results;
    }
    return null;
  }

  static Future<PermissionStatus> _requestPermission(permissions) async {
    var statuses = await request(permissions);
    if (statuses is PermissionStatus) {
      return statuses;
    }

    if (statuses is Map<Permission, PermissionStatus>) {
      var result = PermissionStatus.granted;
      statuses.forEach((key, value) async {
        if (!value.isGranted) {
          result = await key.status;
        }
      });
      return result;
    }
    return PermissionStatus.denied;
  }
}