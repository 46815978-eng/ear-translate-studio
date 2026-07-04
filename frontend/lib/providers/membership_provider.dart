import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:woxueshe/config/api_config.dart';
import 'package:woxueshe/models/membership_model.dart';
import 'package:woxueshe/services/api_service.dart';

class MembershipProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  List<MembershipModel> _plans = [];
  List<MembershipModel> get plans => _plans;

  Future<void> fetchPlans() async {
    final response = await _apiService.get(membershipPlansUrl);
    final body = json.decode(response.body);
    if (body['code'] == 0 && body['data'] != null) {
      _plans = (body['data'] as List).map((json) => MembershipModel.fromJson(json)).toList();
      notifyListeners();
    }
  }

  Future<bool> purchasePlan(int planId) async {
    final response = await _apiService.post(purchaseMembershipUrl,
        body: {'plan_id': planId.toString()}, isForm: true);
    final body = json.decode(response.body);
    return body['code'] == 0;
  }
}
