import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:woxueshe/providers/auth_provider.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});
  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthProvider>(context);
    return Scaffold(
      appBar: AppBar(title: const Text('我的')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(auth.user?.username ?? '未登录', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => auth.logout(),
              child: const Text('退出登录'),
            ),
          ],
        ),
      ),
    );
  }
}
