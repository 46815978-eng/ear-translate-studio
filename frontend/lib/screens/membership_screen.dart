import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:woxueshe/providers/membership_provider.dart';

class MembershipScreen extends StatefulWidget {
  const MembershipScreen({super.key});

  @override
  State<MembershipScreen> createState() => _MembershipScreenState();
}

class _MembershipScreenState extends State<MembershipScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() =>
        Provider.of<MembershipProvider>(context, listen: false).fetchPlans());
  }

  @override
  Widget build(BuildContext context) {
    final mp = Provider.of<MembershipProvider>(context);

    return Scaffold(
      appBar: AppBar(title: const Text('会员中心')),
      body: mp.plans.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: mp.plans.length,
              itemBuilder: (context, index) {
                final plan = mp.plans[index];
                return Card(
                  child: ListTile(
                    title: Text(plan.name),
                    subtitle: Text('${(plan.priceCents / 100).toStringAsFixed(0)} 元 / ${plan.durationDays} 天'),
                    trailing: ElevatedButton(
                      onPressed: () => mp.purchasePlan(plan.id),
                      child: const Text('购买'),
                    ),
                  ),
                );
              },
            ),
    );
  }
}
