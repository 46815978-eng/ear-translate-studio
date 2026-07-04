import 'package:flutter/material.dart';
import 'package:woxueshe/config/theme.dart';
import 'package:woxueshe/providers/auth_provider.dart';
import 'package:provider/provider.dart';
import 'package:woxueshe/screens/splash_screen.dart';
import 'package:woxueshe/screens/login_screen.dart';
import 'package:woxueshe/screens/register_screen.dart';
import 'package:woxueshe/screens/home_screen.dart';
import 'package:woxueshe/screens/course_list_screen.dart';
import 'package:woxueshe/screens/course_detail_screen.dart';
import 'package:woxueshe/screens/listening_screen.dart';
import 'package:woxueshe/screens/review_screen.dart';
import 'package:woxueshe/screens/membership_screen.dart';
import 'package:woxueshe/screens/payment_screen.dart';
import 'package:woxueshe/screens/profile_screen.dart';
import 'package:woxueshe/screens/study_stats_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AuthProvider(),
      child: Consumer<AuthProvider>(
        builder: (_, authProvider, __) {
          return MaterialApp(
            title: '磨耳AI课堂',
            theme: ThemeData(
              colorScheme: ColorScheme.fromSeed(
                seedColor: AppTheme.primaryColor,
                brightness: Brightness.light,
              ),
              useMaterial3: true,
            ),
            darkTheme: ThemeData(
              colorScheme: ColorScheme.fromSeed(
                seedColor: AppTheme.primaryColor,
                brightness: Brightness.dark,
              ),
              useMaterial3: true,
            ),
            home: SplashScreen(),
            routes: {
              '/login': (context) => LoginScreen(),
              '/register': (context) => RegisterScreen(),
              '/home': (context) => HomeScreen(),
              '/course_list': (context) => CourseListScreen(),
              '/listening': (context) => ListeningScreen(),
              '/review': (context) => ReviewScreen(),
              '/membership': (context) => MembershipScreen(),
              '/payment': (context) => PaymentScreen(),
              '/profile': (context) => ProfileScreen(),
              '/study_stats': (context) => StudyStatsScreen(),
            },
          );
        },
      ),
    );
  }
}
