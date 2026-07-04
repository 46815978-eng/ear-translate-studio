import 'package:flutter/material.dart';
import 'package:woxueshe/models/user_model.dart';
import 'package:woxueshe/services/api_service.dart';

class AuthProvider with ChangeNotifier {
  bool _isLoggedIn = false;
  UserModel? _user;

  bool get isLoggedIn => _isLoggedIn;
  UserModel? get user => _user;

  Future<bool> login(String username, String password) async {
    final apiService = ApiService();
    final success = await apiService.login(username, password);
    if (success) {
      _isLoggedIn = true;
      notifyListeners();
    }
    return success;
  }

  Future<bool> register(String username, String email, String password) async {
    final apiService = ApiService();
    final success = await apiService.register(username, email, password);
    if (success) {
      return await login(username, password);
    }
    return false;
  }

  Future<void> logout() async {
    final apiService = ApiService();
    await apiService.logout();
    _isLoggedIn = false;
    _user = null;
    notifyListeners();
  }

  Future<void> checkLoginStatus() async {
    final apiService = ApiService();
    final token = await apiService.getToken();
    _isLoggedIn = token != null && token.isNotEmpty;
    notifyListeners();
  }
}
