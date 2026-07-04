import 'package:flutter/material.dart';

class CourseDetailScreen extends StatefulWidget {
  final int courseId;
  const CourseDetailScreen({super.key, required this.courseId});

  @override
  State<CourseDetailScreen> createState() => _CourseDetailScreenState();
}

class _CourseDetailScreenState extends State<CourseDetailScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('课程详情')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('课程 ID: ${widget.courseId}', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 16),
            const Text('章节列表（待后端接口返回数据后渲染）'),
            // TODO: 接入 courseProvider.getCourseSections(widget.courseId)
          ],
        ),
      ),
    );
  }
}
