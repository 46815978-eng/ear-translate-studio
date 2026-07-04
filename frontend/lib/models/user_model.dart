class UserModel {
  final int id;
  final String username;
  final String email;
  final String avatarUrl;
  final bool isActive;
  final bool isVip;
  final DateTime vipExpireAt;

  UserModel({
    required this.id,
    required this.username,
    required this.email,
    required this.avatarUrl,
    required this.isActive,
    required this.isVip,
    required this.vipExpireAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      username: json['username'],
      email: json['email'],
      avatarUrl: json['avatar_url'],
      isActive: json['is_active'],
      isVip: json['is_vip'],
      vipExpireAt: DateTime.parse(json['vip_expire_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'avatar_url': avatarUrl,
      'is_active': isActive,
      'is_vip': isVip,
      'vip_expire_at': vipExpireAt.toIso8601String(),
    };
  }
}