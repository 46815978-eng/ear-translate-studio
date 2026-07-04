import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:woxueshe/providers/course_provider.dart';
import 'package:woxueshe/models/course_model.dart';
import 'package:woxueshe/screens/course_detail_screen.dart';

class CourseListScreen extends StatefulWidget {
  const CourseListScreen({super.key});

  @override
  State<CourseListScreen> createState() => _CourseListScreenState();
}

class _CourseListScreenState extends State<CourseListScreen> {
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
      appBar: AppBar(title: const Text('课程列表')),
      body: courseProvider.loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: courseProvider.courses.length,
              itemBuilder: (context, index) {
                final course = courseProvider.courses[index];
                return ListTile(
                  title: Text(course.title),
                  subtitle: Text(course.description),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => CourseDetailScreen(courseId: course.id),
                      ),
                    );
                  },
                );
              },
            ),
    );
  }
}
