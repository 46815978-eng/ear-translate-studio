import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:woxueshe/config/api_config.dart';
import 'package:woxueshe/models/course_model.dart';
import 'package:woxueshe/services/api_service.dart';

class CourseProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  List<CourseModel> _courses = [];
  List<CourseModel> get courses => _courses;
  bool _loading = false;
  bool get loading => _loading;

  Future<List<CourseModel>> fetchCourses() async {
    _loading = true;
    notifyListeners();
    final response = await _apiService.get(coursesUrl);
    final body = json.decode(response.body);
    if (body['code'] == 0 && body['data'] != null) {
      _courses = (body['data'] as List).map((json) => CourseModel.fromJson(json)).toList();
    }
    _loading = false;
    notifyListeners();
    return _courses;
  }

  Future<CourseModel?> getCourseDetails(int courseId) async {
    final response = await _apiService.get('$coursesUrl/$courseId');
    final body = json.decode(response.body);
    if (body['code'] == 0 && body['data'] != null) {
      return CourseModel.fromJson(body['data']);
    }
    return null;
  }

  Future<List<dynamic>> getCourseSections(int courseId) async {
    final response = await _apiService.get('$courseSectionsUrl/$courseId/sections');
    final body = json.decode(response.body);
    if (body['code'] == 0 && body['data'] != null) {
      return body['data'];
    }
    return [];
  }
}
