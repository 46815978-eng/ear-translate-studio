import 'package:flutter/material.dart';
import 'package:woxueshe/config/theme.dart';

Widget buildRaisedButton(String label, VoidCallback onPressed) {
  return ElevatedButton(
    onPressed: onPressed,
    child: Text(label),
    style: ElevatedButton.styleFrom(
      primary: AppTheme.primaryColor,
      onPrimary: Colors.white,
    ),
  );
}

Widget buildTextField(String labelText, TextEditingController controller) {
  return TextField(
    controller: controller,
    decoration: InputDecoration(labelText: labelText),
  );
}