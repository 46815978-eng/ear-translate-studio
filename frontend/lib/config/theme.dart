import 'package:flutter/material.dart';

class AppTheme {
  static const Color primaryColor = Color(0xFF4A90D9);
  static const Color secondaryColor = Color(0xFFE8F4FF);
}

final ThemeData lightTheme = ThemeData(
  useMaterial3: true,
  colorScheme: const ColorScheme.light(
    primary: AppTheme.primaryColor,
    secondary: AppTheme.secondaryColor,
  ),
);

final ThemeData darkTheme = ThemeData(
  useMaterial3: true,
  colorScheme: const ColorScheme.dark(
    primary: AppTheme.primaryColor,
    secondary: AppTheme.secondaryColor,
  ),
);