import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:woxueshe/config/api_config.dart';
import 'package:woxueshe/models/user_model.dart';

class ApiService {
  final http.Client _client = http.Client();
  final FlutterSecureStorage _storage = FlutterSecureStorage();

  Future<Map<String, dynamic>> _parseResponse(http.Response response) async {
    final body = json.decode(response.body);
    if (body is Map && body['code'] == 0) {
      return {'success': true, 'data': body['data'], 'message': body['message']};
    }
    return {'success': false, 'data': null, 'message': body is Map ? body['message'] : 'Unknown error'};
  }

  Future<http.Response> get(String url, {Map<String, String>? headers}) async {
    headers = headers ?? {};
    final token = await _storage.read(key: 'token');
    if (token != null) {
      headers['Authorization'] = 'Bearer $token';
    }
    return _client.get(Uri.parse(url), headers: headers);
  }

  Future<http.Response> post(String url, {Map<String, String>? headers, dynamic body, bool isForm = false}) async {
    headers = headers ?? {};
    final token = await _storage.read(key: 'token');
    if (token != null) {
      headers['Authorization'] = 'Bearer $token';
    }
    if (isForm) {
      headers['Content-Type'] = 'application/x-www-form-urlencoded';
      return _client.post(Uri.parse(url), headers: headers, body: body);
    }
    headers['Content-Type'] = 'application/json';
    return _client.post(Uri.parse(url), headers: headers, body: json.encode(body));
  }

  Future<bool> login(String username, String password) async {
    final response = await post(loginUrl,
        body: {'username': username, 'password': password}, isForm: true);
    if (response.statusCode == 200) {
      final body = json.decode(response.body);
      if (body['access_token'] != null) {
        await _storage.write(key: 'token', value: body['access_token']);
        return true;
      }
    }
    return false;
  }

  Future<bool> register(String username, String email, String password) async {
    final response = await post(registerUrl,
        body: {'username': username, 'email': email, 'password': password, 'role': 'student'});
    final result = await _parseResponse(response);
    return result['success'];
  }

  Future<Map<String, dynamic>> getCourses() async {
    final response = await get(coursesUrl);
    return _parseResponse(response);
  }

  Future<Map<String, dynamic>> getMembershipPlans() async {
    final response = await get(membershipPlansUrl);
    return _parseResponse(response);
  }

  Future<String?> getToken() async {
    return _storage.read(key: 'token');
  }

  Future<void> logout() async {
    await _storage.delete(key: 'token');
  }
}
