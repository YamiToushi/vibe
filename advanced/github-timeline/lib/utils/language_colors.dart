import 'package:flutter/material.dart';

/// Language → hex color, sourced from GitHub's Linguist.
const Map<String, Color> languageColors = {
  'Dart':         Color(0xFF00B4AB),
  'Python':       Color(0xFF3572A5),
  'JavaScript':   Color(0xFFF1E05A),
  'TypeScript':   Color(0xFF3178C6),
  'Java':         Color(0xFFB07219),
  'Kotlin':       Color(0xFFA97BFF),
  'Swift':        Color(0xFFF05138),
  'Go':           Color(0xFF00ADD8),
  'Rust':         Color(0xFFDEA584),
  'C':            Color(0xFF555555),
  'C++':          Color(0xFFF34B7D),
  'C#':           Color(0xFF178600),
  'HTML':         Color(0xFFE34C26),
  'CSS':          Color(0xFF563D7C),
  'SCSS':         Color(0xFFC6538C),
  'Ruby':         Color(0xFF701516),
  'PHP':          Color(0xFF4F5D95),
  'Shell':        Color(0xFF89E051),
  'PowerShell':   Color(0xFF012456),
  'Vue':          Color(0xFF41B883),
  'Svelte':       Color(0xFFFF3E00),
  'Lua':          Color(0xFF000080),
  'Haskell':      Color(0xFF5E5086),
  'Scala':        Color(0xFFDC322F),
  'R':            Color(0xFF198CE7),
  'MATLAB':       Color(0xFFE16737),
  'Dockerfile':   Color(0xFF384D54),
  'Makefile':     Color(0xFF427819),
  'Jupyter Notebook': Color(0xFFDA5B0B),
};

Color langColor(String? lang) =>
    (lang != null ? languageColors[lang] : null) ?? const Color(0xFF8E8E93);

/// 10 distinct accessible colors for year badges (cycles by index).
const List<Color> yearPalette = [
  Color(0xFF0969DA), // blue
  Color(0xFF1A7F37), // green
  Color(0xFFBF8700), // yellow
  Color(0xFFCF222E), // red
  Color(0xFF8250DF), // purple
  Color(0xFF0550AE), // dark blue
  Color(0xFF116329), // dark green
  Color(0xFF953800), // orange
  Color(0xFF82071E), // dark red
  Color(0xFF6639BA), // dark purple
];

Color yearColor(int year) => yearPalette[year % yearPalette.length];
