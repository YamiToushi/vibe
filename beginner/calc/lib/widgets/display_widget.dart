import 'package:flutter/material.dart';

class DisplayWidget extends StatelessWidget {
  final String? previousValue;
  final String? operator;
  final String value;

  const DisplayWidget({
    super.key,
    required this.value,
    this.previousValue,
    this.operator,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.centerRight,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: const Color(0xFF16213E),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          if (previousValue != null && operator != null)
            Text(
              '$previousValue $operator',
              style: const TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.w400,
                color: Color(0xFFA9A9A9),
              ),
            ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 64,
              fontWeight: FontWeight.bold,
              fontFamily: 'Roboto',
              fontFeatures: [FontFeature.tabularFigures()],
            ),
            textAlign: TextAlign.right,
          ),
        ],
      ),
    );
  }
}