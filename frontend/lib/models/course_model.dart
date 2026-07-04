class CourseModel {
  final int id;
  final String title;
  final String description;
  final String coverUrl;
  final String difficulty;
  final int durationSeconds;
  final String category;
  final bool status;

  CourseModel({
    required this.id,
    required this.title,
    required this.description,
    required this.coverUrl,
    required this.difficulty,
    required this.durationSeconds,
    required this.category,
    required this.status,
  });

  factory CourseModel.fromJson(Map<String, dynamic> json) {
    return CourseModel(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      coverUrl: json['cover_url'],
      difficulty: json['difficulty'],
      durationSeconds: json['duration_seconds'],
      category: json['category'],
      status: json['status'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'cover_url': coverUrl,
      'difficulty': difficulty,
      'duration_seconds': durationSeconds,
      'category': category,
      'status': status,
    };
  }
}