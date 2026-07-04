class StudyRecordModel {
  final int id;
  final int userId;
  final int courseId;
  final int sectionId;
  final DateTime studyDate;
  final int reviewCount;
  final double easeFactor;
  final int intervalDays;
  final DateTime nextReviewAt;
  final String status;

  StudyRecordModel({
    required this.id,
    required this.userId,
    required this.courseId,
    required this.sectionId,
    required this.studyDate,
    required this.reviewCount,
    required this.easeFactor,
    required this.intervalDays,
    required this.nextReviewAt,
    required this.status,
  });

  factory StudyRecordModel.fromJson(Map<String, dynamic> json) {
    return StudyRecordModel(
      id: json['id'],
      userId: json['user_id'],
      courseId: json['course_id'],
      sectionId: json['section_id'],
      studyDate: DateTime.parse(json['study_date']),
      reviewCount: json['review_count'],
      easeFactor: json['ease_factor'],
      intervalDays: json['interval_days'],
      nextReviewAt: DateTime.parse(json['next_review_at']),
      status: json['status'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'course_id': courseId,
      'section_id': sectionId,
      'study_date': studyDate.toIso8601String(),
      'review_count': reviewCount,
      'ease_factor': easeFactor,
      'interval_days': intervalDays,
      'next_review_at': nextReviewAt.toIso8601String(),
      'status': status,
    };
  }
}