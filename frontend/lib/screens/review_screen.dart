import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:woxueshe/config/api_config.dart';
import 'package:woxueshe/services/api_service.dart';

class ReviewScreen extends StatefulWidget {
  const ReviewScreen({super.key});
  @override
  State<ReviewScreen> createState() => _ReviewScreenState();
}

class _ReviewScreenState extends State<ReviewScreen> {
  List<dynamic> _dueItems = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadDue();
  }

  Future<void> _loadDue() async {
    final api = ApiService();
    final response = await api.get('$baseUrl/review/due');
    final body = json.decode(response.body);
    if (body['code'] == 0 && body['data'] != null) {
      setState(() {
        _dueItems = body['data'];
        _loading = false;
      });
    } else {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('复习')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _dueItems.isEmpty
              ? const Center(child: Text('暂无待复习内容，太棒了！'))
              : ListView.builder(
                  itemCount: _dueItems.length,
                  itemBuilder: (context, index) {
                    final item = _dueItems[index];
                    return ListTile(
                      title: Text('课程 ${item['course_id']}'),
                      subtitle: Text('下次复习: ${item['next_review_at'] ?? '未知'}'),
                      trailing: IconButton(
                        icon: const Icon(Icons.check),
                        onPressed: () async {
                          // Submit review with quality=4 (good)
                          final api = ApiService();
                          await api.post('$baseUrl/review/submit?record_id=${item['id']}&quality=4',
                              isForm: true);
                          _loadDue();
                        },
                      ),
                    );
                  },
                ),
    );
  }
}
