import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:woxueshe/providers/auth_provider.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _userCtrl = TextEditingController();
  final _passCtrl = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('登录')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            TextField(controller: _userCtrl, decoration: const InputDecoration(labelText: '用户名')),
            TextField(controller: _passCtrl, obscureText: true, decoration: const InputDecoration(labelText: '密码')),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () async {
                final auth = Provider.of<AuthProvider>(context, listen: false);
                final ok = await auth.login(_userCtrl.text, _passCtrl.text);
                if (ok) {
                  Navigator.pushReplacementNamed(context, '/home');
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('登录失败')));
                }
              },
              child: const Text('登录'),
            ),
            TextButton(
              onPressed: () => Navigator.pushNamed(context, '/register'),
              child: const Text('没有账号？注册'),
            ),
          ],
        ),
      ),
    );
  }
}
