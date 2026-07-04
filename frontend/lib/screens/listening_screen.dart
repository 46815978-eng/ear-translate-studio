import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:woxueshe/config/api_config.dart';
import 'package:woxueshe/services/api_service.dart';
import 'package:woxueshe/providers/auth_provider.dart';

class ListeningScreen extends StatefulWidget {
  const ListeningScreen({super.key});
  @override
  State<ListeningScreen> createState() => _ListeningScreenState();
}

class _ListeningScreenState extends State<ListeningScreen> {
  List<dynamic> _courses = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadCourses();
  }

  Future<void> _loadCourses() async {
    final api = ApiService();
    final response = await api.get('$baseUrl/listening/courses?mode=random');
    final body = json.decode(response.body);
    if (body['code'] == 0 && body['data'] != null) {
      setState(() {
        _courses = body['data']['items'] ?? [];
        _loading = false;
      });
    } else {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('磨耳朵')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _courses.length,
              itemBuilder: (context, index) {
                final c = _courses[index];
                return ListTile(
                  title: Text(c['title'] ?? '课程'),
                  subtitle: Text(c['description'] ?? ''),
                );
              },
            ),
    );
  }
}
