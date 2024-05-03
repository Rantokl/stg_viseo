import 'package:sav/common/utils/app.utils.dart';
import 'package:sav/models/domain_object/base.do.dart';
import 'package:sav/models/factory/base.factory.dart';
import 'package:sav/repository/local/base_local.repo.dart';

class BaseLocalSA<Do extends BaseDo, Dto,
Factory extends BaseFactory<Do, Dto>,
Repository extends BaseLocalRepo<Do>> {

  late Factory factory;
  late Repository repository;

  initialize({
    required Factory factory,
    required Repository repository
  }) {
    this.factory = factory;
    this.repository = repository;
  }

  _insert(
      Do domainObject,
      CompletionClosure<bool>? completion,
      CompletionClosure<int>? dataId
      ) {
    repository.insert(domainObject).then((result) {
      if(result != null){
        completion?.call(result > 0);
        dataId?.call(result);
      } else {
        completion?.call(false);
        dataId?.call(-1);
      }
    });
  }

  _update(
      Do domainObject,
      CompletionClosure<bool>? completion,
      CompletionClosure<int>? dataId
      ) {
    repository.update(domainObject).then((result) {
      if(result != null){
        completion?.call(result > 0);
        dataId?.call(result);
      } else {
        completion?.call(false);
        dataId?.call(-1);
      }
    });
  }

  insertOrUpdate({
    required Dto data,
    CompletionClosure<bool>? completion,
    CompletionClosure<int>? dataId
  }) async {
    if (data != null) {
      var domainObject = factory.toDomainObject(data);
      bool isNew = true;

      if(domainObject != null){
        if (domainObject?.localId != null) {
          isNew = await findById(domainObject?.localId) == null;
        }
        isNew ? _insert(domainObject, completion, dataId) : _update(
            domainObject, completion, dataId
        );
      } else completion?.call(false);
    } else completion?.call(false);
  }

  insertOrUpdateBatch({
    required List<Dto> data,
    CompletionClosure<bool>? completion
  }) {
    if (data != null) {
      var domainObjects = factory.toDomainObjects(data);
      if(domainObjects != null){
        repository.insertOrUpdateBatch(domainObjects).then((result) {
          completion?.call(result == null);
        });
      } else completion?.call(false);
    } else completion?.call(false);
  }

  Future<Dto?> findById(dynamic id) async {
    var result = await repository.findById(id);
    return (result == null) ? null : factory.toDataTransfertObject(result);
  }

  Future<List<Dto?>> findAll() async {
    List<BaseDo> result = await repository.findAll();
    if (result == null) return [];

    return factory.toDataTransfertObjects(
        result.where((item) => item != null).toList()
    );
  }

  Future<List<Dto?>?> findByCriteria(Map<String, dynamic> criteria, {
    String operator = "AND"
  }) async {
    var result = await repository.findByCriteria(
        criteria,
        operator: operator
    );
    return (result == null) ? null : factory.toDataTransfertObjects(result);
  }

  delete({required Dto data, CompletionClosure<bool>? completion}) {
    if (data != null) {
      var domainObject = factory.toDomainObject(data);
      if(domainObject != null){
        repository.delete(domainObject).then((result) {
          if(result != null)
            completion?.call(result > 0);
          else
            completion?.call(false);
        });
      } else completion?.call(false);
    } else completion?.call(false);
  }

  deleteBatch({required List<Dto> data, CompletionClosure<bool>? completion}) {
    if (data != null) {
      var domainObjects = factory.toDomainObjects(data);
      if(domainObjects != null){
        repository.deleteBatch(domainObjects).then((result) {
          completion?.call(result.where((it) => it == 0).isEmpty);
        });
      } else completion?.call(false);
    } else completion?.call(false);
  }

  deleteAll({CompletionClosure<bool>? completion}) {
    repository.deleteAll().then((result) {
      if (result != null)
        completion?.call(result > 0);
      else
        completion?.call(false);
    });
  }

}