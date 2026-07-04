import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:woxueshe/providers/auth_provider.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});
  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _userCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();
  final _passCtrl = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('注册')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            TextField(controller: _userCtrl, decoration: const InputDecoration(labelText: '用户名')),
            TextField(controller: _emailCtrl, decoration: const InputDecoration(labelText: '邮箱')),
            TextField(controller: _passCtrl, obscureText: true, decoration: const InputDecoration(labelText: '密码')),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () async {
                final auth = Provider.of<AuthProvider>(context, listen: false);
                final ok = await auth.register(_userCtrl.text, _emailCtrl.text, _passCtrl.text);
                if (ok) {
                  Navigator.pushReplacementNamed(context, '/home');
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('注册失败')));
                }
              },
              child: const Text('注册'),
            ),
          ],
        ),
      ),
    );
  }
}
