class MembershipModel {
  final int id;
  final String name;
  final int priceCents;
  final int durationDays;
  final String description;
  final Map<String, dynamic> features;

  MembershipModel({
    required this.id,
    required this.name,
    required this.priceCents,
    required this.durationDays,
    required this.description,
    required this.features,
  });

  factory MembershipModel.fromJson(Map<String, dynamic> json) {
    return MembershipModel(
      id: json['id'],
      name: json['name'],
      priceCents: json['price_cents'],
      durationDays: json['duration_days'],
      description: json['description'],
      features: json['features_json'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'price_cents': priceCents,
      'duration_days': durationDays,
      'description': description,
      'features_json': features,
    };
  }
}