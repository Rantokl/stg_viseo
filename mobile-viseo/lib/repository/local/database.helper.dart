import 'package:sav/common/utils/app.log.dart';
import 'package:sav/models/base_synchonizable.dart';
import 'package:sav/models/domain_object/base.do.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseHelper {
  final name = "viseo.db";
  final version = 1;

  final String _typeInt = "INT";
  final String _typeText = "TEXT";
  final String _typeReal = "REAL";

  AppLog loger = AppLog.instance;

  static final DatabaseHelper _instance = DatabaseHelper._internal();

  factory DatabaseHelper() => _instance;

  DatabaseHelper._internal();

  static DatabaseHelper get instance => DatabaseHelper();

  static Database? _database;

  Future<Database?> get database async {
    if (_database == null) {
      _database = await initDatabase();
    }
    return _database;
  }

  Future<String> get path async {
    var filePath = await getDatabasesPath();
    return join(filePath, name);
  }

  initDatabase() async {
    return await openDatabase(
        await path,
        version: version,
        onCreate: onCreate
    );
  }

  onCreate(Database db, int version) async {

  }

  close() async {
    _database?.close();
    _database = null;
  }

  deleteDb() async {
    _database = null;
    return await deleteDatabase(await path);
  }

  String? _creatingTableText<Do extends BaseDo>(Do domainObject, {
    String idKey = localIdKey,
    bool autoIncrement = true
  }) {
    if (domainObject != null) {
      var json = domainObject?.toJsonLocal();
      var tableText = "";

      json?.remove(idKey);

      json?.forEach((key, value) {
        if (value != null) {
          var type = "";
          if (value is int) {
            type = _typeInt;
          } else if (value is double) {
            type = _typeReal;
          } else if (value is String) {
            type = _typeText;
          }
          tableText = "$tableText, $key $type";
        }
      });

      var result = "CREATE TABLE ${domainObject.runtimeType} "
          "($idKey INTEGER PRIMARY KEY"
          "${autoIncrement ? " AUTOINCREMENT" : ""}$tableText)";

      loger.print(tag: "SQL", data: result);

      return result;
    }
    return null;
  }
}