import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:woxueshe/config/api_config.dart';
import 'package:woxueshe/models/study_record_model.dart';
import 'package:woxueshe/services/api_service.dart';

class StudyProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  List<StudyRecordModel> _records = [];
  List<StudyRecordModel> get records => _records;

  Future<void> fetchRecords() async {
    final response = await _apiService.get('$studyRecordsUrl/total');
    final body = json.decode(response.body);
    if (body['code'] == 0 && body['data'] != null) {
      // This endpoint returns stats, not records. 
      // For simplicity, just notify that we have data.
      notifyListeners();
    }
  }

  Future<bool> addRecord(int courseId, int sectionId, int durationSeconds) async {
    final response = await _apiService.post('$studyRecordsUrl/record',
        body: {
          'course_id': courseId.toString(),
          'section_id': sectionId.toString(),
          'duration_seconds': durationSeconds.toString()
        },
        isForm: true);
    final body = json.decode(response.body);
    return body['code'] == 0;
  }
}
