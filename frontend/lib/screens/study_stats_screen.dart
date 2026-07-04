import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class StudyStatsScreen extends StatelessWidget {
  const StudyStatsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('学习统计')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('本周学习时长', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 16),
            SizedBox(
              height: 200,
              child: LineChart(
                LineChartData(
                  lineBarsData: [
                    LineChartBarData(
                      spots: const [
                        FlSpot(0, 1),
                        FlSpot(1, 1.5),
                        FlSpot(2, 2),
                        FlSpot(3, 1.8),
                        FlSpot(4, 2.5),
                        FlSpot(5, 3),
                        FlSpot(6, 2.2),
                      ],
                      color: Colors.blue,
                      barWidth: 3,
                      isCurved: true,
                    ),
                  ],
                  titlesData: FlTitlesData(
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        getTitlesWidget: (value, meta) => Text(
                          ['一','二','三','四','五','六','日'][value.toInt() % 7],
                          style: const TextStyle(fontSize: 10),
                        ),
                      ),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: true, reservedSize: 40),
                    ),
                    topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                    rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
