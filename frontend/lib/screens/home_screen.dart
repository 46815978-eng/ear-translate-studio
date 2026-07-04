import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:woxueshe/providers/course_provider.dart';
import 'package:woxueshe/providers/auth_provider.dart';
import 'package:woxueshe/screens/course_list_screen.dart';
import 'package:woxueshe/screens/listening_screen.dart';
import 'package:woxueshe/screens/review_screen.dart';
import 'package:woxueshe/screens/membership_screen.dart';
import 'package:woxueshe/screens/study_stats_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() =>
        Provider.of<CourseProvider>(context, listen: false).fetchCourses());
  }

  @override
  Widget build(BuildContext context) {
    final courseProvider = Provider.of<CourseProvider>(context);

    return Scaffold(
      appBar: AppBar(title: const Text('磨耳AI课堂')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('推荐课程', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 8),
          courseProvider.loading
              ? const Center(child: CircularProgressIndicator())
              : SizedBox(
                  height: 200,
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    itemCount: courseProvider.courses.length,
                    itemBuilder: (context, index) {
                      final c = courseProvider.courses[index];
                      return Card(
                        child: Container(
                          width: 160,
                          padding: const EdgeInsets.all(8),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(c.title, style: Theme.of(context).textTheme.titleMedium),
                              const SizedBox(height: 4),
                              Text(c.description, maxLines: 2, overflow: TextOverflow.ellipsis),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
          const SizedBox(height: 24),
          Text('功能入口', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 8),
          Wrap(
            spacing: 12,
            children: [
              _buildFeatureCard(context, Icons.headphones, '磨耳朵', () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => const ListeningScreen()));
              }),
              _buildFeatureCard(context, Icons.refresh, '复习', () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => const ReviewScreen()));
              }),
              _buildFeatureCard(context, Icons.card_membership, '会员', () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => const MembershipScreen()));
              }),
              _buildFeatureCard(context, Icons.bar_chart, '学习统计', () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => const StudyStatsScreen()));
              }),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildFeatureCard(BuildContext context, IconData icon, String label, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [Icon(icon, size: 32), const SizedBox(height: 8), Text(label)],
          ),
        ),
      ),
    );
  }
}
