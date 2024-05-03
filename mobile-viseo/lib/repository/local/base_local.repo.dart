import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/common/utils/app.log.dart';
import 'package:sav/models/base_synchonizable.dart';
import 'package:sav/models/domain_object/base.do.dart';
import 'package:sav/repository/local/database.helper.dart';
import 'package:sqflite/sqlite_api.dart';


class BaseLocalRepo<Do extends BaseDo>{
  Future<Database?> get database => DatabaseHelper.instance.database;
  AppLog loger = AppLog.instance;

  late DataCreator<Do> _creator;
  String _localIdKey = localIdKey;

  String get table => _creator().runtimeType.toString();

  BaseLocalRepository({
    required DataCreator<Do> creator,
    String localIdKey = localIdKey
  }) {
    this._creator = creator;
    this._localIdKey = localIdKey;
  }

  ///insert an item
  Future<int?> insert(Do data) async {
    var db = await database;
    return await db?.insert(
        table, data.toJsonLocal()
    );
  }

  ///update an item
  Future<int?> update(Do data) async {
    var db = await database;
    var result = await db?.update(
        table,
        data.toJsonLocal(),
        where: "$_localIdKey = ?",
        whereArgs: <dynamic>[data.currentLocalId]
    );
    return result;
  }

  ///insert or update multiple data
  Future<List<int>> insertOrUpdateBatch(List<Do?> data) async {
    var db = await database;
    var response;
    try {
      var batch = db?.batch();
      for(var item in data) {
        try {
          if(item != null){
            batch?.insert(
                table,
                item.toJsonLocal(),
                conflictAlgorithm: ConflictAlgorithm.replace
            );
          }
        } catch (error) {
          loger.print(tag: "SQL",data: "INSERT ERROR ON $error");
        }
      }
      response = await batch?.commit(noResult: true);
      loger.print(tag: "SQL",data: "INSERT/UPDATE BATCH ${response.toString()}");
    } catch (error) {
      response = [];
      loger.print(tag: "SQL",data: "INSERT BATCH ERROR $error");
    }
    return response;
  }

  ///delete one object
  Future<int?> delete(Do data) async {
    var db = await database;
    return await db?.delete(
        table,
        where: "$_localIdKey = ?",
        whereArgs: <dynamic>[data.currentLocalId]
    );
  }

  ///delete list of objects
  Future<List<int>> deleteBatch(List<Do?> data) async {
    var db = await database;
    List<int> responses = [];
    var response;
    try {
      await db?.transaction((db) async {
        data.forEach((item) async {
          try {
            if(item != null){
              var resTemp = await delete(item);
              responses.add(resTemp!);
            }
          } catch (error) {
            loger.print(tag: "SQL",data: "DELETE ERROR ON $error");
          }
        });
      });
      response = responses;
      loger.print(tag: "SQL",data: "DELETE BATCH $response");
    } catch (error) {
      response = [];
      loger.print(tag: "SQL",data: "DELETE BATCH ERROR $error");
    }
    return response;
  }

  ///delete all rows on database (according to table)
  Future<int?> deleteAll() async {
    var db = await database;
    return db?.delete(table);
  }

  ///select all data from database
  Future<List<BaseDo>> findAll() async {
    var db = await database;
    var map = await db?.query(table);
    List<BaseDo> result = [];
    map?.forEach((data) {
      if (data != null) {
        result.add(_creator().fromJson(data));
      }
    });
    return result;
  }

  ///select data according to criteria
  Future<List<BaseDo>> findByCriteria(Map<String, dynamic> criteria, {
    String operator = "AND"
  }) async {
    var db = await database;
    var criteriaString = "";
    criteria.forEach((key, value) {
      criteriaString += "$key = ? $operator ";
    });
    criteriaString =
        criteriaString
            .trim()
            .substring(
            0,
            criteriaString
                .trim()
                .length - operator.length
        ).trim();
    loger.print(tag: "SQL",data: "${this.runtimeType} CRITERIA STRING : $criteriaString");
    var map = await db?.query(
        table,
        where: criteriaString,
        whereArgs: criteria.values.toList()
    );

    if (map!.isEmpty) {
      return [];
    }
    List<BaseDo> result = [];
    map?.forEach((data) {
      if (data != null) {
        result.add(_creator().fromJson(data));
      }
    });
    return result;
  }

  ///find item by localId
  Future<BaseDo?> findById(dynamic localId) async {
    var db = await database;
    var map = await db?.query(
        table,
        where: "$_localIdKey = ?",
        whereArgs: [localId]
    );
    if (map!.isEmpty) {
      return null;
    }
    return _creator().fromJson(map?.first);
  }

}